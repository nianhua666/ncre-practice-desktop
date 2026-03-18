from __future__ import annotations

import json
import threading
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

from .ai_provider import AIProvider, AIProviderError, DEFAULT_AI_SETTINGS
from .config import APP_NAME, APP_VERSION, frontend_dir
from .database import Database
from .exam_engine import ExamEngine
from .question_bank import QuestionBankService


class ApplicationContext:
    def __init__(self) -> None:
        self.database = Database()
        self.question_bank_service = QuestionBankService()
        self.exam_engine = ExamEngine(self.question_bank_service)
        self.ai_provider = AIProvider(lambda: self.database.get_setting("ai_settings", DEFAULT_AI_SETTINGS))

    def get_settings(self) -> dict[str, Any]:
        settings = dict(DEFAULT_AI_SETTINGS)
        settings.update(self.database.get_setting("ai_settings", {}))
        return settings

    def save_settings(self, payload: dict[str, Any]) -> dict[str, Any]:
        settings = dict(DEFAULT_AI_SETTINGS)
        settings.update(payload)
        self.database.set_setting("ai_settings", settings)
        return settings

    def test_settings(self, payload: dict[str, Any]) -> dict[str, Any]:
        settings = dict(DEFAULT_AI_SETTINGS)
        settings.update(payload)
        return self.ai_provider.test_connection(settings)

    def get_dashboard(self) -> dict[str, Any]:
        attempts = self.database.list_attempts()
        detailed_attempts = self.database.list_attempt_payloads(limit=50)
        summary = self.question_bank_service.dashboard_summary(attempts)
        summary["weak_topics"] = self.question_bank_service.analyze_weak_topics(detailed_attempts)
        summary["topic_mastery"] = self.question_bank_service.analyze_topic_mastery(detailed_attempts)
        summary["study_recommendations"] = self.question_bank_service.build_study_recommendations(detailed_attempts)
        summary["wrong_book_preview"] = self.question_book_preview(detailed_attempts)
        summary["app_name"] = APP_NAME
        summary["app_version"] = APP_VERSION
        return summary

    def question_book_preview(self, detailed_attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        preview = self.question_bank_service.build_wrong_book(detailed_attempts, limit=6, include_question=False)
        for item in preview:
            item.pop("analysis", None)
            item.pop("latest_user_answer", None)
        return preview

    def generate_system_exam(
        self,
        subject_code: str,
        seed: int | None = None,
        focus_topic: str | None = None,
        weakness_boost: bool = False,
    ) -> dict[str, Any]:
        prioritized_topics: list[str] = []
        if weakness_boost:
            attempts = self.database.list_attempt_payloads(subject_code=subject_code, limit=30)
            prioritized_topics = [
                item["topic"]
                for item in self.question_bank_service.analyze_weak_topics(attempts, subject_code=subject_code)[:3]
            ]
        return self.exam_engine.generate_system_exam_with_options(
            subject_code,
            seed=seed,
            focus_topic=focus_topic,
            prioritized_topics=prioritized_topics,
        )

    def generate_ai_exam(self, subject_code: str) -> dict[str, Any]:
        subject = self.question_bank_service.get_subject(subject_code)
        generated = self.ai_provider.generate_exam(subject)
        return self.exam_engine.build_ai_exam(subject_code, generated)

    def get_wrong_book(self, subject_code: str, limit: int = 30) -> list[dict[str, Any]]:
        attempts = self.database.list_attempt_payloads(subject_code=subject_code, limit=100)
        return self.question_bank_service.build_wrong_book(
            attempts,
            subject_code=subject_code,
            limit=limit,
            include_question=False,
        )

    def generate_wrong_book_exam(self, subject_code: str, limit: int = 15) -> dict[str, Any]:
        subject = self.question_bank_service.get_subject(subject_code)
        attempts = self.database.list_attempt_payloads(subject_code=subject_code, limit=100)
        wrong_book = self.question_bank_service.build_wrong_book(
            attempts,
            subject_code=subject_code,
            limit=limit,
            include_question=True,
        )
        if not wrong_book:
            raise ValueError("当前没有可用于重练的错题记录。")

        questions = [item["question"] for item in wrong_book if item.get("question")]
        total_score = sum(question.get("score", 0) for question in questions)
        high_frequency_count = sum(1 for question in questions if question.get("frequency") == "high")
        type_counts: dict[str, int] = {}
        for question in questions:
            question_type = question["type"]
            type_counts[question_type] = type_counts.get(question_type, 0) + 1

        return {
            "exam_id": f"wrong-{uuid4().hex}",
            "subject_code": subject_code,
            "subject_name": subject["name"],
            "source": "wrong_book",
            "title": f"{subject['name']} 错题重练",
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "blueprint": {
                "duration_minutes": max(20, len(questions) * 4),
                "mode": "wrong_book",
                "quotas": [{"type": key, "count": value} for key, value in sorted(type_counts.items())],
            },
            "questions": questions,
            "total_score": total_score,
            "high_frequency_count": high_frequency_count,
            "focus_topic": None,
            "prioritized_topics": [],
        }

    def submit_exam(self, payload: dict[str, Any]) -> dict[str, Any]:
        exam = payload["exam"]
        answers = payload.get("answers", {})
        settings = self.get_settings()
        ai_feedback_lookup: dict[str, dict[str, Any]] = {}
        ai_used = False
        should_use_ai_review = settings.get("enabled") and (
            settings.get("enable_ai_review") or settings.get("grading_mode") == "ai_first"
        )

        for question in exam["questions"]:
            if question["type"] not in {"short_answer", "bug_fix", "programming"}:
                continue
            answer_text = str(answers.get(question["id"], "")).strip()
            if not answer_text or not should_use_ai_review:
                continue
            try:
                ai_feedback_lookup[question["id"]] = self.ai_provider.grade_subjective_question(question, answer_text)
                ai_used = True
            except AIProviderError as exc:
                ai_feedback_lookup[question["id"]] = {
                    "score": 0,
                    "reason": str(exc),
                    "strengths": [],
                    "mistakes": ["AI 批改失败，已回退到题库规则评分。"],
                    "improvement_suggestions": [],
                }

        result = self.exam_engine.grade_exam(exam, answers, ai_feedback_lookup=ai_feedback_lookup)

        if settings.get("enabled") and settings.get("grading_mode") == "ai_first":
            for item in result["question_results"]:
                feedback = item.get("ai_feedback")
                if feedback and item["question_type"] in {"short_answer", "bug_fix", "programming"}:
                    item["obtained_score"] = feedback["score"]
                    item["is_correct"] = feedback["score"] >= item["max_score"] * 0.8
            count = result["summary"]["question_count"]
            result["summary"]["obtained_score"] = round(
                sum(item["obtained_score"] for item in result["question_results"]),
                2,
            )
            result["summary"]["correct_count"] = sum(
                1 for item in result["question_results"] if item["is_correct"]
            )
            result["summary"]["correct_rate"] = round(
                result["summary"]["correct_count"] / count,
                4,
            ) if count else 0.0
            ai_used = True

        attempt_id = f"attempt-{uuid4().hex}"
        submitted_at = datetime.now().isoformat(timespec="seconds")
        self.database.insert_attempt(
            {
                "id": attempt_id,
                "subject_code": exam["subject_code"],
                "subject_name": exam["subject_name"],
                "exam_mode": exam["source"],
                "title": exam["title"],
                "started_at": payload.get("started_at") or exam["started_at"],
                "submitted_at": submitted_at,
                "total_score": result["summary"]["total_score"],
                "obtained_score": result["summary"]["obtained_score"],
                "correct_rate": result["summary"]["correct_rate"],
                "ai_used": ai_used,
                "blueprint": exam["blueprint"],
                "exam": exam,
                "answers": answers,
                "result": result,
            }
        )
        return {"attempt_id": attempt_id, "submitted_at": submitted_at, "result": result}


class NCREHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], context: ApplicationContext) -> None:
        self.context = context
        super().__init__(server_address, NCRERequestHandler)


class NCRERequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(frontend_dir()), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/subjects":
            self._send_json(self.server.context.question_bank_service.list_subjects())
            return
        if parsed.path == "/api/dashboard":
            self._send_json(self.server.context.get_dashboard())
            return
        if parsed.path == "/api/resources":
            self._send_json(self.server.context.question_bank_service.list_resources())
            return
        if parsed.path == "/api/settings":
            self._send_json(self.server.context.get_settings())
            return
        if parsed.path.startswith("/api/topics/"):
            subject_code = parsed.path.rsplit("/", 1)[-1]
            self._send_json(self.server.context.question_bank_service.list_topics(subject_code))
            return
        if parsed.path == "/api/wrong-book":
            query = parse_qs(parsed.query)
            subject_code = query.get("subject_code", [None])[0]
            if not subject_code:
                self._send_json({"error": "缺少 subject_code。"}, status=HTTPStatus.BAD_REQUEST)
                return
            limit = int(query.get("limit", ["30"])[0])
            self._send_json(self.server.context.get_wrong_book(subject_code, limit=limit))
            return
        if parsed.path == "/api/history":
            query = parse_qs(parsed.query)
            subject_code = query.get("subject_code", [None])[0]
            self._send_json(self.server.context.database.list_attempts(subject_code))
            return
        if parsed.path.startswith("/api/history/"):
            attempt_id = parsed.path.rsplit("/", 1)[-1]
            payload = self.server.context.database.get_attempt(attempt_id)
            if not payload:
                self._send_json({"error": "未找到对应考试记录。"}, status=HTTPStatus.NOT_FOUND)
                return
            self._send_json(payload)
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        payload = self._read_json()
        if self.path == "/api/exams/system":
            try:
                exam = self.server.context.generate_system_exam(
                    payload.get("subject_code"),
                    seed=payload.get("seed"),
                    focus_topic=payload.get("focus_topic"),
                    weakness_boost=bool(payload.get("weakness_boost")),
                )
                self._send_json(exam)
            except Exception as exc:  # noqa: BLE001
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return
        if self.path == "/api/exams/ai":
            try:
                exam = self.server.context.generate_ai_exam(payload.get("subject_code"))
                self._send_json(exam)
            except Exception as exc:  # noqa: BLE001
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return
        if self.path == "/api/exams/wrong-book":
            try:
                exam = self.server.context.generate_wrong_book_exam(
                    payload.get("subject_code"),
                    limit=int(payload.get("limit", 15)),
                )
                self._send_json(exam)
            except Exception as exc:  # noqa: BLE001
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return
        if self.path == "/api/exams/submit":
            try:
                result = self.server.context.submit_exam(payload)
                self._send_json(result)
            except Exception as exc:  # noqa: BLE001
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return
        if self.path == "/api/settings/test":
            try:
                result = self.server.context.test_settings(payload)
                self._send_json(result)
            except Exception as exc:  # noqa: BLE001
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return
        self._send_json({"error": "不支持的接口。"}, status=HTTPStatus.NOT_FOUND)

    def do_PUT(self) -> None:  # noqa: N802
        if self.path != "/api/settings":
            self._send_json({"error": "不支持的接口。"}, status=HTTPStatus.NOT_FOUND)
            return
        settings = self.server.context.save_settings(self._read_json())
        self._send_json(settings)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _read_json(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def start_server(
    context: ApplicationContext | None = None,
    host: str = "127.0.0.1",
    port: int = 0,
) -> tuple[NCREHTTPServer, threading.Thread, str]:
    app_context = context or ApplicationContext()
    server = NCREHTTPServer((host, port), app_context)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://{host}:{server.server_port}"


def open_desktop(address: str, use_webview: bool = True) -> None:
    if use_webview:
        try:
            import webview  # type: ignore

            webview.create_window(APP_NAME, address, min_size=(1180, 760))
            webview.start()
            return
        except Exception:  # noqa: BLE001
            pass
    webbrowser.open(address)
