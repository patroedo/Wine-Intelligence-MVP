"""Gemini wine-label recognition adapter.

Architecture inspired by Cork Dork (MIT):
https://github.com/BaconWappedBitcoin/ha-wine-cellar

Server-side only: never expose GEMINI_API_KEY to the browser.
"""
from __future__ import annotations

import base64
import json
import os
import re
from typing import Any

import requests

DEFAULT_MODEL = os.getenv("GEMINI_WINE_MODEL", "gemini-2.5-flash")

LABEL_PROMPT = """You are a wine label recognition expert. Analyze the supplied bottle/label photo.
Return ONLY JSON with: producer, wine_name, vintage, appellation, region, country, grapes, confidence, visible_text.
Rules: never invent unreadable fields; use null when unknown; vintage is a four digit integer or null; confidence is 0..1; visible_text is a short transcription of text actually visible. If this is not a wine bottle/label return {\"error\":\"not_a_wine_label\"}."""


def _parse_json(text: str) -> dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I | re.S).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            raise
        data = json.loads(re.sub(r",\s*([}\]])", r"\1", m.group(0)))
    if not isinstance(data, dict):
        raise ValueError("Vision response is not a JSON object")
    return data


def recognize_label(image_bytes: bytes, mime_type: str = "image/jpeg", *, api_key: str | None = None, model: str = DEFAULT_MODEL, timeout: int = 45) -> dict[str, Any]:
    """Recognize one wine label with Gemini Vision and return normalized JSON."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    if not image_bytes:
        raise ValueError("Empty image")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [
            {"text": LABEL_PROMPT},
            {"inline_data": {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode("ascii")}},
        ]}],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"},
    }
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    body = r.json()
    candidates = body.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no candidates")
    parts = ((candidates[0].get("content") or {}).get("parts") or [])
    text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
    result = _parse_json(text)
    if "confidence" in result and result["confidence"] is not None:
        try:
            result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))
        except (TypeError, ValueError):
            result["confidence"] = None
    result["provider"] = "gemini"
    result["model"] = model
    return result
