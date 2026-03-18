from __future__ import annotations

import json
import subprocess
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXE_PATH = ROOT / "dist" / "NCREPractice" / "NCREPractice.exe"
PORT = 18766


def main() -> int:
    if not EXE_PATH.exists():
        raise FileNotFoundError(f"未找到 EXE：{EXE_PATH}")

    process = subprocess.Popen(
        [str(EXE_PATH), "--serve", "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        time.sleep(3)
        dashboard = json.loads(
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/dashboard", timeout=10)
            .read()
            .decode("utf-8")
        )
        if dashboard["subject_count"] < 1 or dashboard["question_count"] < 1:
            raise RuntimeError("打包版启动成功，但 dashboard 数据异常。")
        print(f"Packaged EXE smoke test passed: {dashboard['subject_count']} subjects, {dashboard['question_count']} questions")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
