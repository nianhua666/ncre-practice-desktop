from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import bundled_data_dir


class QuestionBankService:
    def __init__(self) -> None:
        self.data_dir = bundled_data_dir()
        self._subjects_cache: list[dict[str, Any]] | None = None
        self._bank_cache: dict[str, dict[str, Any]] = {}

    def _subjects_file(self) -> Path:
        return self.data_dir / "subjects.json"

    def _resources_file(self) -> Path:
        return self.data_dir / "resources.json"

    def list_subjects(self) -> list[dict[str, Any]]:
        if self._subjects_cache is None:
            with self._subjects_file().open("r", encoding="utf-8") as handle:
                self._subjects_cache = json.load(handle)
        return deepcopy(self._subjects_cache)

    def list_resources(self) -> list[dict[str, Any]]:
        with self._resources_file().open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def get_subject(self, subject_code: str) -> dict[str, Any]:
        for subject in self.list_subjects():
            if subject["code"] == subject_code:
                return subject
        raise KeyError(f"未找到科目：{subject_code}")

    def load_bank(self, subject_code: str) -> dict[str, Any]:
        if subject_code in self._bank_cache:
            return deepcopy(self._bank_cache[subject_code])
        subject = self.get_subject(subject_code)
        bank_path = self.data_dir / "question_banks" / subject["bank_file"]
        with bank_path.open("r", encoding="utf-8") as handle:
            bank = json.load(handle)
        self._bank_cache[subject_code] = bank
        return deepcopy(bank)

    def list_topics(self, subject_code: str) -> list[str]:
        bank = self.load_bank(subject_code)
        counter = Counter(question.get("topic") for question in bank["questions"] if question.get("topic"))
        return [topic for topic, _ in counter.most_common()]

    def analyze_weak_topics(self, attempt_payloads: list[dict[str, Any]], subject_code: str | None = None) -> list[dict[str, Any]]:
        counter: Counter[str] = Counter()
        for payload in attempt_payloads:
            if subject_code and payload.get("subject_code") != subject_code:
                continue
            result = payload.get("result", {})
            for item in result.get("question_results", []):
                topic = item.get("topic")
                if not topic:
                    continue
                if item.get("is_correct"):
                    continue
                weight = 2 if item.get("frequency") == "high" else 1
                counter[topic] += weight
        return [
            {"topic": topic, "mistake_weight": count}
            for topic, count in counter.most_common(10)
        ]

    def analyze_topic_mastery(
        self,
        attempt_payloads: list[dict[str, Any]],
        subject_code: str | None = None,
    ) -> list[dict[str, Any]]:
        mastery: dict[str, dict[str, Any]] = {}
        for payload in attempt_payloads:
            if subject_code and payload.get("subject_code") != subject_code:
                continue
            for item in payload.get("result", {}).get("question_results", []):
                topic = item.get("topic")
                if not topic:
                    continue
                entry = mastery.setdefault(
                    topic,
                    {
                        "topic": topic,
                        "correct_count": 0,
                        "total_count": 0,
                        "weighted_correct": 0,
                        "weighted_total": 0,
                    },
                )
                weight = 2 if item.get("frequency") == "high" else 1
                entry["total_count"] += 1
                entry["weighted_total"] += weight
                if item.get("is_correct"):
                    entry["correct_count"] += 1
                    entry["weighted_correct"] += weight

        items = []
        for entry in mastery.values():
            total = entry["total_count"]
            weighted_total = entry["weighted_total"] or 1
            items.append(
                {
                    "topic": entry["topic"],
                    "correct_count": entry["correct_count"],
                    "total_count": total,
                    "accuracy": round(entry["correct_count"] / total, 4) if total else 0.0,
                    "weighted_accuracy": round(entry["weighted_correct"] / weighted_total, 4),
                }
            )
        items.sort(key=lambda item: (item["weighted_accuracy"], item["total_count"]))
        return items

    def build_study_recommendations(
        self,
        attempt_payloads: list[dict[str, Any]],
        subject_code: str | None = None,
        limit: int = 6,
    ) -> list[dict[str, Any]]:
        weak_topics = {
            item["topic"]: item["mistake_weight"]
            for item in self.analyze_weak_topics(attempt_payloads, subject_code=subject_code)
        }
        mastery_items = self.analyze_topic_mastery(attempt_payloads, subject_code=subject_code)

        recommendations: list[dict[str, Any]] = []
        for item in mastery_items:
            topic = item["topic"]
            accuracy = item["weighted_accuracy"]
            total_count = item["total_count"]
            mistake_weight = weak_topics.get(topic, 0)
            if total_count < 2 and mistake_weight == 0:
                continue

            if accuracy < 0.45:
                priority = "high"
                action = "优先做专题冲刺，再做错题重练"
            elif accuracy < 0.7:
                priority = "medium"
                action = "保持专题刷题，并结合弱项补刷"
            else:
                priority = "low"
                action = "保持少量复习，防止生疏"

            recommendations.append(
                {
                    "topic": topic,
                    "priority": priority,
                    "weighted_accuracy": accuracy,
                    "total_count": total_count,
                    "mistake_weight": mistake_weight,
                    "action": action,
                }
            )

        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(
            key=lambda item: (
                priority_order[item["priority"]],
                item["weighted_accuracy"],
                -item["mistake_weight"],
                -item["total_count"],
            )
        )
        return recommendations[:limit]

    def build_study_plan_markdown(
        self,
        subject: dict[str, Any],
        attempt_payloads: list[dict[str, Any]],
    ) -> str:
        weak_topics = self.analyze_weak_topics(attempt_payloads, subject_code=subject["code"])
        topic_mastery = self.analyze_topic_mastery(attempt_payloads, subject_code=subject["code"])
        recommendations = self.build_study_recommendations(attempt_payloads, subject_code=subject["code"])
        wrong_book = self.build_wrong_book(attempt_payloads, subject_code=subject["code"], limit=20, include_question=False)

        lines = [
            f"# {subject['name']} 复习计划",
            "",
            f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- 题库题量：{subject['question_count']}",
            f"- 高频题量：{subject.get('high_frequency_question_count', 0)}",
            f"- 题库完整度：{subject['completeness']}",
            "",
            "## 自动复习建议",
        ]
        if recommendations:
            for item in recommendations:
                lines.append(
                    f"- {item['topic']}：优先级 `{item['priority']}`，加权正确率 {item['weighted_accuracy']:.0%}，建议 {item['action']}"
                )
        else:
            lines.append("- 当前答题数据不足，继续刷题后再导出会更有价值。")

        lines.extend(["", "## 高频弱项"])
        if weak_topics:
            for item in weak_topics:
                lines.append(f"- {item['topic']}：错题权重 {item['mistake_weight']}")
        else:
            lines.append("- 暂无高频弱项统计。")

        lines.extend(["", "## 专题掌握度"])
        if topic_mastery:
            for item in topic_mastery[:12]:
                lines.append(
                    f"- {item['topic']}：加权正确率 {item['weighted_accuracy']:.0%}，原始正确率 {item['accuracy']:.0%}，作答 {item['total_count']} 次"
                )
        else:
            lines.append("- 暂无专题掌握度统计。")

        lines.extend(["", "## 错题本重点"])
        if wrong_book:
            for item in wrong_book:
                lines.append(
                    f"- {item['question_id']} [{item.get('topic') or item['type']}]：错 {item['wrong_count']} 次，最近错误时间 {item['last_wrong_at']}"
                )
                lines.append(f"  题干：{item['stem']}")
        else:
            lines.append("- 当前还没有错题本记录。")

        return "\n".join(lines) + "\n"

    def build_wrong_book_markdown(
        self,
        subject: dict[str, Any],
        attempt_payloads: list[dict[str, Any]],
    ) -> str:
        wrong_book = self.build_wrong_book(attempt_payloads, subject_code=subject["code"], limit=50, include_question=False)
        lines = [
            f"# {subject['name']} 错题本",
            "",
            f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- 错题条目：{len(wrong_book)}",
            "",
        ]
        if not wrong_book:
            lines.append("当前还没有错题记录。")
            return "\n".join(lines) + "\n"

        for item in wrong_book:
            lines.append(f"## {item['question_id']} · {item.get('topic') or item['type']}")
            lines.append(f"- 错误次数：{item['wrong_count']}")
            lines.append(f"- 高频考点：{'是' if item.get('frequency') == 'high' else '否'}")
            lines.append(f"- 最近错误时间：{item['last_wrong_at']}")
            lines.append(f"- 题干：{item['stem']}")
            if item.get("analysis"):
                lines.append(f"- 解析：{item['analysis']}")
            lines.append("")

        return "\n".join(lines)

    def build_wrong_book(
        self,
        attempt_payloads: list[dict[str, Any]],
        subject_code: str | None = None,
        limit: int | None = None,
        include_question: bool = True,
    ) -> list[dict[str, Any]]:
        aggregated: dict[str, dict[str, Any]] = {}

        for payload in attempt_payloads:
            if subject_code and payload.get("subject_code") != subject_code:
                continue

            question_lookup = {
                question["id"]: question
                for question in payload.get("exam", {}).get("questions", [])
            }

            for item in payload.get("result", {}).get("question_results", []):
                if item.get("is_correct"):
                    continue

                question_id = item["question_id"]
                question = question_lookup.get(question_id, {})
                entry = aggregated.setdefault(
                    question_id,
                    {
                        "question_id": question_id,
                        "type": question.get("type", item.get("question_type")),
                        "topic": item.get("topic") or question.get("topic"),
                        "frequency": item.get("frequency") or question.get("frequency", "medium"),
                        "stem": question.get("stem", ""),
                        "score": question.get("score", item.get("max_score", 0)),
                        "wrong_count": 0,
                        "last_wrong_at": payload.get("submitted_at") or payload.get("started_at"),
                        "latest_user_answer": item.get("user_answer"),
                        "analysis": item.get("analysis", ""),
                        "question": deepcopy(question) if include_question else None,
                    },
                )
                entry["wrong_count"] += 1
                entry["latest_user_answer"] = item.get("user_answer")
                entry["analysis"] = item.get("analysis", entry["analysis"])
                last_wrong_at = payload.get("submitted_at") or payload.get("started_at")
                if last_wrong_at and last_wrong_at > (entry["last_wrong_at"] or ""):
                    entry["last_wrong_at"] = last_wrong_at
                    if include_question and question:
                        entry["question"] = deepcopy(question)

        items = list(aggregated.values())
        items.sort(
            key=lambda item: (
                item["wrong_count"],
                1 if item.get("frequency") == "high" else 0,
                item.get("last_wrong_at") or "",
            ),
            reverse=True,
        )
        if limit:
            items = items[:limit]

        if not include_question:
            for item in items:
                item.pop("question", None)
        return items

    def dashboard_summary(self, attempts: list[dict[str, Any]]) -> dict[str, Any]:
        subjects = self.list_subjects()
        total_questions = sum(subject["question_count"] for subject in subjects)
        total_attempts = len(attempts)
        average_score = round(
            sum(item["obtained_score"] for item in attempts) / total_attempts,
            2,
        ) if attempts else 0.0
        average_correct_rate = round(
            sum(item["correct_rate"] for item in attempts) / total_attempts,
            4,
        ) if attempts else 0.0
        return {
            "subject_count": len(subjects),
            "question_count": total_questions,
            "attempt_count": total_attempts,
            "average_score": average_score,
            "average_correct_rate": average_correct_rate,
            "latest_attempts": attempts[:5],
            "subjects": subjects,
        }
