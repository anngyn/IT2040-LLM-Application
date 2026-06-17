"""Flexible LLM clients for offline, API, and optional local-model runs."""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Protocol
from urllib import request


class LLMClient(Protocol):
    provider: str
    model: str

    def generate(self, prompt: str, case: Dict[str, Any]) -> str:
        ...


@dataclass
class GeminiClient:
    """Minimal Gemini REST client using models.generateContent."""

    api_key: str
    model: str
    base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    provider: str = "gemini"
    temperature: float = 0.0
    timeout_seconds: int = 60

    def generate(self, prompt: str, case: Dict[str, Any]) -> str:
        url = f"{self.base_url.rstrip('/')}/models/{self.model}:generateContent"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": self.temperature},
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            method="POST",
        )
        start = time.perf_counter()
        with request.urlopen(req, timeout=self.timeout_seconds) as response:
            body = response.read().decode("utf-8")
        elapsed = time.perf_counter() - start
        parsed = json.loads(body)
        candidates = parsed.get("candidates", [])
        if not candidates:
            raise RuntimeError("Gemini response did not include any candidates.")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts if isinstance(part, dict))
        return text.strip() + f"\n\n<!-- api_latency_seconds={elapsed:.3f} -->"


@dataclass
class MockFactCheckClient:
    """Offline deterministic client used for smoke tests and cached demos."""

    model: str = "mock-fact-audit-heuristic"
    provider: str = "mock"

    def generate(self, prompt: str, case: Dict[str, Any]) -> str:
        claim = str(case.get("source_claim", ""))
        aux = str(case.get("auxiliary_info", ""))
        evidence_text = f"{claim}\n{aux}".lower()

        negative_patterns = [
            r"\brefuted\b",
            r"\bfake\b",
            r"\bhoax\b",
            r"\bfalse\b",
            r"\bno evidence\b",
            r"\bnot official\b",
            r"\bdid not\b",
        ]
        positive_patterns = [
            r"\bsupported\b",
            r"\bconfirmed\b",
            r"\baccurate\b",
            r"\btrue\b",
            r"\bshows that\b",
        ]

        if aux and any(re.search(pattern, evidence_text) for pattern in negative_patterns):
            verdict = "Non-Factual"
            reason = (
                "The supplied auxiliary evidence contains refuting signals, credibility warnings, "
                "or explicit statements that undermine the source claim."
            )
        elif aux and any(re.search(pattern, evidence_text) for pattern in positive_patterns):
            verdict = "Factual"
            reason = (
                "The supplied auxiliary evidence contains supporting signals and factual details "
                "that align with the source claim."
            )
        elif not aux:
            verdict = "Not Enough Information"
            reason = (
                "No auxiliary information is available in claim-only mode, so the claim cannot "
                "be verified reliably by this offline baseline."
            )
        else:
            verdict = "Not Enough Information"
            reason = (
                "The auxiliary information provides context but no decisive support or refutation, "
                "so this offline baseline abstains from a factual verdict."
            )

        return json.dumps(
            {
                "verdict": verdict,
                "justification": reason,
            },
            ensure_ascii=False,
        )


@dataclass
class OpenAICompatibleClient:
    """Minimal OpenAI-compatible chat completion client using urllib."""

    api_key: str
    model: str
    base_url: str = "https://api.openai.com/v1"
    provider: str = "openai"
    temperature: float = 0.0
    timeout_seconds: int = 60

    def generate(self, prompt: str, case: Dict[str, Any]) -> str:
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        start = time.perf_counter()
        with request.urlopen(req, timeout=self.timeout_seconds) as response:
            body = response.read().decode("utf-8")
        elapsed = time.perf_counter() - start
        parsed = json.loads(body)
        content = parsed["choices"][0]["message"]["content"]
        return content.strip() + f"\n\n<!-- api_latency_seconds={elapsed:.3f} -->"


@dataclass
class TransformersClient:
    """Optional local Hugging Face causal-LM client."""

    model_path: str
    model: str
    provider: str = "transformers"
    max_new_tokens: int = 512

    def __post_init__(self) -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch

        self._torch = torch
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self._model = AutoModelForCausalLM.from_pretrained(self.model_path)
        self._model.eval()

    def generate(self, prompt: str, case: Dict[str, Any]) -> str:
        inputs = self._tokenizer(prompt, return_tensors="pt")
        with self._torch.no_grad():
            output = self._model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
            )
        return self._tokenizer.decode(output[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True)


def build_client(
    *,
    provider: str,
    model: str,
    base_url: str | None = None,
    temperature: float = 0.0,
    timeout_seconds: int = 60,
    model_path: str | None = None,
) -> LLMClient:
    provider = (provider or "mock").strip().lower()
    if provider == "mock":
        return MockFactCheckClient(model=model or "mock-fact-audit-heuristic")
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY or LLM_API_KEY is required for provider=gemini")
        return GeminiClient(
            api_key=api_key,
            model=model,
            base_url=base_url or os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"),
            temperature=temperature,
            timeout_seconds=timeout_seconds,
        )
    if provider in {"openai", "openai_compatible", "api"}:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY or LLM_API_KEY is required for provider=openai")
        return OpenAICompatibleClient(
            api_key=api_key,
            model=model,
            base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            temperature=temperature,
            timeout_seconds=timeout_seconds,
        )
    if provider in {"transformers", "local"}:
        resolved_model_path = model_path or os.getenv("LOCAL_MODEL_PATH") or model
        return TransformersClient(model_path=resolved_model_path, model=model)
    raise ValueError(f"Unsupported LLM provider: {provider}")
