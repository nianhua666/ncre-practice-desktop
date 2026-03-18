from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def analyze(subject_code: str) -> None:
    path = ROOT / "data" / "question_banks" / f"{subject_code}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    questions = payload["questions"]
    by_type = Counter(question["type"] for question in questions)
    by_frequency = Counter(question.get("frequency", "medium") for question in questions)
    by_topic = Counter(question.get("topic", "unknown") for question in questions)
    total_score = sum(question.get("score", 0) for question in questions)
    high_ratio = round(by_frequency.get("high", 0) / len(questions), 4) if questions else 0.0

    print(f"Subject: {payload['subject_name']}")
    print(f"Question count: {len(questions)}")
    print(f"Total score across bank: {total_score}")
    print(f"High-frequency ratio: {high_ratio:.2%}")
    print("By type:")
    for key, value in sorted(by_type.items()):
        print(f"  {key}: {value}")
    print("By frequency:")
    for key, value in sorted(by_frequency.items()):
        print(f"  {key}: {value}")
    print("Top topics:")
    for key, value in by_topic.most_common(12):
        print(f"  {key}: {value}")


if __name__ == "__main__":
    analyze("level2_c")
