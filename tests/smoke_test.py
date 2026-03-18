from __future__ import annotations

import unittest

from backend.ai_provider import DEFAULT_AI_SETTINGS
from backend.app import ApplicationContext
from backend.question_bank import QuestionBankService


class SmokeTest(unittest.TestCase):
    def test_subjects_and_banks_exist(self) -> None:
        service = QuestionBankService()
        subjects = service.list_subjects()
        self.assertGreaterEqual(len(subjects), 5)
        level2c = service.get_subject("level2_c")
        self.assertEqual(level2c["completeness"], "broad")
        self.assertGreaterEqual(level2c["high_frequency_question_count"], 390)
        bank = service.load_bank("level2_c")
        self.assertGreaterEqual(len(bank["questions"]), 420)
        self.assertGreaterEqual(
            sum(1 for item in bank["questions"] if item.get("frequency") == "high"),
            390,
        )

    def test_system_exam_generation(self) -> None:
        context = ApplicationContext()
        exam = context.generate_system_exam("level2_c", seed=20260318)
        self.assertEqual(exam["subject_code"], "level2_c")
        self.assertEqual(exam["source"], "system")
        self.assertEqual(len(exam["questions"]), 30)
        self.assertEqual(exam["total_score"], 105)
        self.assertGreaterEqual(exam["high_frequency_count"], 18)
        self.assertIsNone(exam["focus_topic"])

    def test_topic_focused_exam_generation(self) -> None:
        context = ApplicationContext()
        focus_topic = "\u5b57\u7b26\u4e32"
        exam = context.generate_system_exam("level2_c", seed=20260318, focus_topic=focus_topic)
        self.assertEqual(exam["focus_topic"], focus_topic)
        self.assertGreaterEqual(
            sum(1 for item in exam["questions"] if item.get("topic") == focus_topic),
            8,
        )

    def test_weakness_boost_generation(self) -> None:
        context = ApplicationContext()
        exam = context.generate_system_exam("level2_c", seed=7)
        answers = {question["id"]: "" for question in exam["questions"]}
        context.submit_exam({"exam": exam, "answers": answers})
        boosted = context.generate_system_exam("level2_c", seed=8, weakness_boost=True)
        self.assertGreaterEqual(len(boosted["prioritized_topics"]), 1)

    def test_wrong_book_exam_generation(self) -> None:
        context = ApplicationContext()
        exam = context.generate_system_exam("level2_c", seed=21)
        answers = {question["id"]: "" for question in exam["questions"]}
        context.submit_exam({"exam": exam, "answers": answers})
        wrong_book = context.get_wrong_book("level2_c", limit=10)
        self.assertGreaterEqual(len(wrong_book), 1)
        remedial = context.generate_wrong_book_exam("level2_c", limit=10)
        self.assertEqual(remedial["source"], "wrong_book")
        self.assertGreaterEqual(len(remedial["questions"]), 1)

    def test_dashboard_topic_mastery(self) -> None:
        context = ApplicationContext()
        exam = context.generate_system_exam("level2_c", seed=33)
        context.submit_exam({"exam": exam, "answers": {question["id"]: "" for question in exam["questions"]}})
        dashboard = context.get_dashboard()
        self.assertGreaterEqual(len(dashboard.get("topic_mastery", [])), 1)
        self.assertGreaterEqual(len(dashboard.get("study_recommendations", [])), 1)

    def test_submit_exam_and_persist(self) -> None:
        context = ApplicationContext()
        context.save_settings(DEFAULT_AI_SETTINGS)
        exam = context.generate_system_exam("level2_c", seed=99)
        answers = {}
        for question in exam["questions"]:
            if question["type"] == "single_choice":
                answers[question["id"]] = question["answer"]
            elif question["type"] in {"fill_blank", "code_completion"}:
                answer = question["answer"]
                answers[question["id"]] = answer[0] if isinstance(answer, list) else answer
            elif question["type"] in {"bug_fix", "short_answer", "programming"}:
                answers[question["id"]] = "\u751f\u547d\u5468\u671f \u5c40\u90e8\u6570\u7ec4 \u60ac\u7a7a\u5730\u5740 \u6307\u9488 fopen fclose \u521d\u59cb\u5316 \u904d\u5386 \u6574\u9664"
        payload = context.submit_exam({"exam": exam, "answers": answers})
        self.assertIn("attempt_id", payload)
        self.assertGreater(payload["result"]["summary"]["obtained_score"], 0)
        detail = context.database.get_attempt(payload["attempt_id"])
        self.assertIsNotNone(detail)


if __name__ == "__main__":
    unittest.main()
