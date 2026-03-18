from __future__ import annotations

import unittest

from backend.ai_provider import AIProvider


class AIProviderCompatibilityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = AIProvider(lambda: {})

    def test_build_endpoint_normalizes_v1(self) -> None:
        endpoint = self.provider._build_endpoint("https://api.openai.com", "responses")
        self.assertEqual(endpoint, "https://api.openai.com/v1/responses")

    def test_build_endpoint_removes_existing_path_suffix(self) -> None:
        endpoint = self.provider._build_endpoint("https://example.com/v1/chat/completions", "chat_completions")
        self.assertEqual(endpoint, "https://example.com/v1/chat/completions")

    def test_sub2api_prefers_chat_completions_in_auto_mode(self) -> None:
        order = self.provider._protocol_attempt_order(
            {
                "protocol": "auto",
                "provider_name": "Sub2API",
                "base_url": "https://sub2api.example.com",
            }
        )
        self.assertEqual(order, ["chat_completions", "responses"])


if __name__ == "__main__":
    unittest.main()
