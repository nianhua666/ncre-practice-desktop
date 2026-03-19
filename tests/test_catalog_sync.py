from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from backend.question_bank import QuestionBankService


class CatalogSyncTest(unittest.TestCase):
    def test_sync_subject_bank_from_local_catalog(self) -> None:
        root = Path(__file__).resolve().parent.parent
        source_bank = root / "data" / "question_banks" / "level2_c.json"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            catalog_path = temp_path / "catalog.json"
            catalog_payload = {
                "version": "test",
                "default_subject_code": "level2_c",
                "subjects": [
                    {
                        "code": "level2_c",
                        "name": "二级 C 语言程序设计",
                        "level": "二级",
                        "question_count": 420,
                        "high_frequency_question_count": 390,
                        "bank_file": "level2_c.json",
                        "sha256": __import__("hashlib").sha256(source_bank.read_bytes()).hexdigest(),
                        "download_url": source_bank.resolve().as_uri(),
                    }
                ],
            }
            catalog_path.write_text(json.dumps(catalog_payload, ensure_ascii=False), encoding="utf-8")

            previous_home = os.environ.get("NCRE_APP_HOME")
            previous_catalog = os.environ.get("NCRE_REMOTE_CATALOG_URL")
            os.environ["NCRE_APP_HOME"] = temp_dir
            os.environ["NCRE_REMOTE_CATALOG_URL"] = catalog_path.resolve().as_uri()
            try:
                service = QuestionBankService()
                result = service.sync_subject_bank("level2_c", force_refresh=True)
                self.assertEqual(result["subject_code"], "level2_c")
                self.assertTrue((temp_path / "question_banks" / "level2_c.json").exists())
            finally:
                if previous_home is None:
                    os.environ.pop("NCRE_APP_HOME", None)
                else:
                    os.environ["NCRE_APP_HOME"] = previous_home
                if previous_catalog is None:
                    os.environ.pop("NCRE_REMOTE_CATALOG_URL", None)
                else:
                    os.environ["NCRE_REMOTE_CATALOG_URL"] = previous_catalog


if __name__ == "__main__":
    unittest.main()
