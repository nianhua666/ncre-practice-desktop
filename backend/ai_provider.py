from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_AI_SETTINGS = {
    "enabled": False,
    "provider_name": "OpenAI Compatible",
    "protocol": "auto",
    "base_url": "https://api.openai.com/v1",
    "api_key": "",
    "model": "gpt-4.1-mini",
    "temperature": 0.2,
    "timeout_seconds": 60,
    "organization": "",
    "project": "",
    "extra_headers": "",
    "grading_mode": "hybrid",
    "enable_ai_review": True,
    "openai_console_url": "https://platform.openai.com/settings/organization/api-keys",
}


class AIProviderError(RuntimeError):
    pass


@dataclass
class AIProviderHTTPError(AIProviderError):
    status_code: int
    detail: str

    def __str__(self) -> str:
        return f"AI 请求失败：HTTP {self.status_code}，{self.detail}"


class AIProvider:
    def __init__(self, settings_getter: Any) -> None:
        self.settings_getter = settings_getter

    def get_settings(self) -> dict[str, Any]:
        settings = dict(DEFAULT_AI_SETTINGS)
        settings.update(self.settings_getter() or {})
        return settings

    def ensure_enabled(self) -> dict[str, Any]:
        settings = self.get_settings()
        if not settings.get("enabled"):
            raise AIProviderError("AI 功能未启用，请先在系统设置中启用并填写 API Key。")
        if not settings.get("api_key"):
            raise AIProviderError("AI API Key 为空，请先在系统设置中配置。")
        return settings

    def request_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        settings = self.ensure_enabled()
        attempts = self._protocol_attempt_order(settings)
        errors: list[str] = []

        for protocol in attempts:
            try:
                return self._request_json_once(settings, system_prompt, user_prompt, protocol)
            except AIProviderHTTPError as exc:
                errors.append(f"{protocol}: {exc}")
                if not self._should_fallback(exc):
                    raise
            except AIProviderError as exc:
                errors.append(f"{protocol}: {exc}")
                raise

        raise AIProviderError("；".join(errors) if errors else "AI 请求失败。")

    def test_connection(self, settings_override: dict[str, Any] | None = None) -> dict[str, Any]:
        settings = self.get_settings()
        if settings_override:
            settings.update(settings_override)
        if not settings.get("enabled"):
            raise AIProviderError("AI 功能未启用，无法测试连接。")
        if not settings.get("api_key"):
            raise AIProviderError("API Key 为空，无法测试连接。")
        result = None
        for protocol in self._protocol_attempt_order(settings):
            try:
                result = self._request_json_once(
                    settings,
                    system_prompt="你是连接测试助手。请只返回 JSON。",
                    user_prompt='请返回 {"ok":true,"message":"connection ok"}',
                    protocol=protocol,
                )
                settings["protocol"] = protocol
                break
            except AIProviderHTTPError as exc:
                if not self._should_fallback(exc):
                    raise
        if result is None:
            raise AIProviderError("连接测试失败。")
        return {
            "provider_name": settings.get("provider_name"),
            "protocol": settings.get("protocol"),
            "base_url": settings.get("base_url"),
            "model": settings.get("model"),
            "result": result,
        }

    def generate_exam(self, subject: dict[str, Any]) -> dict[str, Any]:
        blueprint = subject["default_blueprint"]
        system_prompt = (
            "你是中国全国计算机等级考试命题助手。"
            "请严格输出 JSON，不要输出 Markdown，不要输出解释。"
        )
        user_prompt = (
            "请生成一套模拟试卷 JSON。\n"
            f"科目：{subject['name']}\n"
            f"考试级别：{subject['level']}\n"
            f"题型配额：{json.dumps(blueprint['quotas'], ensure_ascii=False)}\n"
            '顶层格式必须为 {"title":"...","blueprint":{"duration_minutes":120,"quotas":[]},"questions":[...]}。\n'
            "每道题必须包含 id,type,stem,score,tags,difficulty,analysis。"
            "选择题必须包含 options 与 answer。"
            "简答、改错、程序设计题必须包含 rubric，rubric 每项含 description,keywords,points。"
        )
        payload = self.request_json(system_prompt, user_prompt)
        payload.setdefault("blueprint", blueprint)
        return payload

    def grade_subjective_question(self, question: dict[str, Any], answer: str) -> dict[str, Any]:
        system_prompt = "你是中国全国计算机等级考试阅卷助手。请严格输出 JSON，不要输出 Markdown。"
        user_prompt = (
            "请根据题目、解析和评分点批改考生答案。\n"
            f"题目：{json.dumps(question, ensure_ascii=False)}\n"
            f"考生答案：{answer}\n"
            '返回 JSON：{"score":0,"reason":"...","strengths":["..."],"mistakes":["..."],"improvement_suggestions":["..."]}'
        )
        payload = self.request_json(system_prompt, user_prompt)
        payload["score"] = max(0, min(question["score"], float(payload.get("score", 0))))
        return payload

    def _request_json_once(
        self,
        settings: dict[str, Any],
        system_prompt: str,
        user_prompt: str,
        protocol: str,
    ) -> dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings['api_key']}",
        }
        if settings.get("organization"):
            headers["OpenAI-Organization"] = settings["organization"]
        if settings.get("project"):
            headers["OpenAI-Project"] = settings["project"]
        headers.update(self._parse_extra_headers(settings.get("extra_headers", "")))

        endpoint = self._build_endpoint(settings["base_url"], protocol)
        if protocol == "chat_completions":
            body = {
                "model": settings["model"],
                "temperature": settings["temperature"],
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }
        else:
            body = {
                "model": settings["model"],
                "temperature": settings["temperature"],
                "input": [
                    {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                    {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
                ],
                "text": {"format": {"type": "json_object"}},
            }

        request = urllib.request.Request(
            endpoint,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        timeout = max(10, int(settings.get("timeout_seconds", 60)))

        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise AIProviderHTTPError(exc.code, detail) from exc
        except urllib.error.URLError as exc:
            raise AIProviderError(f"AI 请求失败：{exc.reason}") from exc

        content = self._extract_json_text(payload)
        if not content:
            raise AIProviderError("AI 返回内容为空，无法解析 JSON。")

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise AIProviderError(f"AI 返回的内容不是有效 JSON：{content[:300]}") from exc

    @staticmethod
    def _parse_extra_headers(extra_headers: str) -> dict[str, str]:
        headers: dict[str, str] = {}
        for line in extra_headers.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        normalized = (base_url or "").strip().rstrip("/")
        for suffix in ("/chat/completions", "/responses"):
            if normalized.endswith(suffix):
                normalized = normalized[: -len(suffix)]
        return normalized

    def _build_endpoint(self, base_url: str, protocol: str) -> str:
        normalized = self._normalize_base_url(base_url)
        if normalized.endswith("/v1"):
            root = normalized
        else:
            root = normalized + "/v1"
        path = "/chat/completions" if protocol == "chat_completions" else "/responses"
        return root + path

    def _protocol_attempt_order(self, settings: dict[str, Any]) -> list[str]:
        protocol = settings.get("protocol", "auto")
        fingerprint = f"{settings.get('provider_name', '')} {settings.get('base_url', '')}".lower()
        if protocol == "auto":
            if "sub2api" in fingerprint:
                return ["chat_completions", "responses"]
            return ["responses", "chat_completions"]
        if protocol == "responses" and "sub2api" in fingerprint:
            return ["responses", "chat_completions"]
        return [protocol]

    @staticmethod
    def _should_fallback(exc: AIProviderHTTPError) -> bool:
        if exc.status_code in {400, 404, 405, 501}:
            lowered = exc.detail.lower()
            markers = ["not found", "unsupported", "unknown", "route", "path", "endpoint"]
            if any(marker in lowered for marker in markers) or exc.status_code in {404, 405, 501}:
                return True
        return False

    def _extract_json_text(self, payload: Any) -> str:
        if isinstance(payload, dict):
            if isinstance(payload.get("output_text"), str):
                return payload["output_text"]
            if isinstance(payload.get("choices"), list) and payload["choices"]:
                choice = payload["choices"][0]
                message = choice.get("message", {})
                if isinstance(message.get("content"), str):
                    return message["content"]
            if isinstance(payload.get("output"), list):
                fragments: list[str] = []
                for item in payload["output"]:
                    if isinstance(item, dict):
                        for content in item.get("content", []):
                            if isinstance(content, dict):
                                if isinstance(content.get("text"), str):
                                    fragments.append(content["text"])
                                elif isinstance(content.get("content"), str):
                                    fragments.append(content["content"])
                if fragments:
                    return "\n".join(fragments)
        return ""
