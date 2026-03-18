from __future__ import annotations

import math
import random
import re
from copy import deepcopy
from datetime import datetime
from typing import Any
from uuid import uuid4


def _normalize_text(value: str) -> str:
    cleaned = re.sub(r"\s+", "", value or "")
    return cleaned.strip().lower()


class ExamEngine:
    def __init__(self, question_bank_service: Any) -> None:
        self.question_bank_service = question_bank_service

    def generate_system_exam(self, subject_code: str, seed: int | None = None) -> dict[str, Any]:
        return self.generate_system_exam_with_options(subject_code, seed=seed)

    def generate_system_exam_with_options(
        self,
        subject_code: str,
        seed: int | None = None,
        focus_topic: str | None = None,
        prioritized_topics: list[str] | None = None,
    ) -> dict[str, Any]:
        bank = self.question_bank_service.load_bank(subject_code)
        subject = self.question_bank_service.get_subject(subject_code)
        blueprint = deepcopy(bank["default_blueprint"])
        rng = random.Random(seed or datetime.now().timestamp())
        questions = self._select_questions(
            bank["questions"],
            blueprint,
            rng,
            focus_topic=focus_topic,
            prioritized_topics=prioritized_topics,
        )
        total_score = sum(question["score"] for question in questions)
        high_frequency_count = sum(1 for question in questions if question.get("frequency") == "high")
        return {
            "exam_id": f"sys-{uuid4().hex}",
            "subject_code": subject_code,
            "subject_name": subject["name"],
            "source": "system",
            "title": self._build_exam_title(subject["name"], focus_topic, prioritized_topics),
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "blueprint": blueprint,
            "questions": questions,
            "total_score": total_score,
            "high_frequency_count": high_frequency_count,
            "focus_topic": focus_topic,
            "prioritized_topics": prioritized_topics or [],
        }

    def build_ai_exam(self, subject_code: str, generated_exam: dict[str, Any]) -> dict[str, Any]:
        subject = self.question_bank_service.get_subject(subject_code)
        questions = generated_exam["questions"]
        total_score = sum(question.get("score", 0) for question in questions)
        high_frequency_count = sum(1 for question in questions if question.get("frequency") == "high")
        return {
            "exam_id": f"ai-{uuid4().hex}",
            "subject_code": subject_code,
            "subject_name": subject["name"],
            "source": "ai",
            "title": generated_exam.get("title") or f"{subject['name']} AI 模拟题",
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "blueprint": generated_exam.get("blueprint", subject["default_blueprint"]),
            "questions": questions,
            "total_score": total_score,
            "high_frequency_count": high_frequency_count,
        }

    def grade_exam(
        self,
        exam_payload: dict[str, Any],
        answers: dict[str, Any],
        ai_feedback_lookup: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        ai_feedback_lookup = ai_feedback_lookup or {}
        question_results: list[dict[str, Any]] = []
        obtained_score = 0.0

        for question in exam_payload["questions"]:
            answer = answers.get(question["id"], "")
            result = self._grade_question(question, answer)
            if question["id"] in ai_feedback_lookup:
                result["ai_feedback"] = ai_feedback_lookup[question["id"]]
            question_results.append(result)
            obtained_score += result["obtained_score"]

        total_score = exam_payload["total_score"]
        correct_count = sum(1 for item in question_results if item["is_correct"])
        correct_rate = round(correct_count / len(question_results), 4) if question_results else 0.0
        return {
            "question_results": question_results,
            "summary": {
                "total_score": total_score,
                "obtained_score": round(obtained_score, 2),
                "correct_count": correct_count,
                "question_count": len(question_results),
                "correct_rate": correct_rate,
            },
        }

    def _select_questions(
        self,
        questions: list[dict[str, Any]],
        blueprint: dict[str, Any],
        rng: random.Random,
        focus_topic: str | None = None,
        prioritized_topics: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        selected: list[dict[str, Any]] = []
        used_ids: set[str] = set()
        prioritized_topics = prioritized_topics or []
        for quota in blueprint["quotas"]:
            candidates = [
                deepcopy(question)
                for question in questions
                if question["type"] == quota["type"] and question["id"] not in used_ids
            ]
            if len(candidates) < quota["count"]:
                raise ValueError(f"{quota['type']} 题量不足，无法生成试卷。")
            high_frequency_candidates = [item for item in candidates if item.get("frequency") == "high"]
            normal_candidates = [item for item in candidates if item.get("frequency") != "high"]
            focus_candidates = [item for item in candidates if self._is_focus_match(item, focus_topic, prioritized_topics)]
            focus_high_candidates = [item for item in focus_candidates if item.get("frequency") == "high"]
            focus_normal_candidates = [item for item in focus_candidates if item.get("frequency") != "high"]
            rng.shuffle(high_frequency_candidates)
            rng.shuffle(normal_candidates)
            rng.shuffle(focus_high_candidates)
            rng.shuffle(focus_normal_candidates)

            high_target = quota.get("high_frequency_target")
            if high_target is None and high_frequency_candidates:
                high_target = max(1, math.ceil(quota["count"] * 0.6))
            high_target = min(high_target or 0, len(high_frequency_candidates), quota["count"])

            chosen: list[dict[str, Any]] = []
            if focus_topic or prioritized_topics:
                focus_target = min(
                    quota["count"],
                    len(focus_candidates),
                    max(1, math.ceil(quota["count"] * (0.75 if focus_topic else 0.45))),
                )
                preferred_focus = focus_high_candidates + focus_normal_candidates
                chosen.extend(preferred_focus[:focus_target])

            current_ids = {item["id"] for item in chosen}
            high_pool = [item for item in high_frequency_candidates if item["id"] not in current_ids]
            chosen.extend(high_pool[: max(0, high_target - len([item for item in chosen if item.get("frequency") == "high"]))])

            if len(chosen) < quota["count"]:
                current_ids = {item["id"] for item in chosen}
                normal_pool = [item for item in normal_candidates if item["id"] not in current_ids]
                chosen.extend(normal_pool[: quota["count"] - len(chosen)])

            if len(chosen) < quota["count"]:
                remaining = [
                    item for item in high_frequency_candidates[high_target:]
                    if item["id"] not in {question["id"] for question in chosen}
                ]
                chosen.extend(remaining[: quota["count"] - len(chosen)])

            selected.extend(chosen)
            used_ids.update(question["id"] for question in chosen)
        rng.shuffle(selected)
        return selected

    @staticmethod
    def _is_focus_match(question: dict[str, Any], focus_topic: str | None, prioritized_topics: list[str]) -> bool:
        topic = question.get("topic")
        if focus_topic and topic == focus_topic:
            return True
        if prioritized_topics and topic in prioritized_topics:
            return True
        return False

    @staticmethod
    def _build_exam_title(subject_name: str, focus_topic: str | None, prioritized_topics: list[str] | None) -> str:
        if focus_topic:
            return f"{subject_name} · {focus_topic} 专题冲刺"
        if prioritized_topics:
            return f"{subject_name} · 弱项强化模拟"
        return f"{subject_name} 模拟考试"

    def _grade_question(self, question: dict[str, Any], user_answer: Any) -> dict[str, Any]:
        question_type = question["type"]
        reference = question.get("answer")
        normalized_user_answer = user_answer if isinstance(user_answer, list) else str(user_answer or "")

        if question_type in {"single_choice", "true_false"}:
            is_correct = str(user_answer).strip().upper() == str(reference).strip().upper()
            obtained_score = question["score"] if is_correct else 0
            analysis = question["analysis"]
        elif question_type == "multiple_choice":
            expected = sorted(reference)
            received = sorted(user_answer) if isinstance(user_answer, list) else []
            is_correct = expected == received
            obtained_score = question["score"] if is_correct else 0
            analysis = question["analysis"]
        elif question_type in {"fill_blank", "code_completion"}:
            accepted_answers = reference if isinstance(reference, list) else [reference]
            normalized_candidates = {_normalize_text(item) for item in accepted_answers}
            is_correct = _normalize_text(normalized_user_answer) in normalized_candidates
            obtained_score = question["score"] if is_correct else 0
            analysis = question["analysis"]
        else:
            rubric = question.get("rubric", [])
            obtained_score = 0.0
            hit_points: list[str] = []
            lowered = _normalize_text(normalized_user_answer)
            for item in rubric:
                variants = item.get("keywords", [])
                if any(_normalize_text(keyword) in lowered for keyword in variants):
                    obtained_score += item["points"]
                    hit_points.append(item["description"])
            obtained_score = min(question["score"], round(obtained_score, 2))
            is_correct = obtained_score >= question["score"] * 0.8
            analysis = question["analysis"]
            if hit_points:
                analysis += "\n命中要点：" + "；".join(hit_points)

        return {
            "question_id": question["id"],
            "question_type": question_type,
            "topic": question.get("topic"),
            "frequency": question.get("frequency", "medium"),
            "expected_answer": reference,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "obtained_score": obtained_score,
            "max_score": question["score"],
            "analysis": analysis,
        }
