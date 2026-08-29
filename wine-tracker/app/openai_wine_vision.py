"""OpenAI Vision adapter for Wine Intelligence.

Server-side only: never expose OPENAI_API_KEY to the browser.
Returns conservative structured wine-label metadata for confirmation.
"""
import base64
import json
import os
import urllib.request
import urllib.error

OPENAI_URL = "https://api.openai.com/v1/responses"

SCHEMA_PROMPT = """Analyze this wine bottle/label photo. Identify only information visible or strongly supported by the label. Do not invent missing facts. Return ONLY valid JSON with this exact shape: {\"producer\":\"\",\"wine_name\":\"\",\"vintage\":\"\",\"appellation\":\"\",\"region\":\"\",\"grapes\":[],\"country\":\"\",\"confidence\":0.0,\"visible_text\":[],\"needs_confirmation\":true}. confidence must be 0..1. If producer/wine/vintage are uncertain leave them empty and set needs_confirmation true."""


def _extract_json(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("Model did not return JSON")
    return json.loads(text[start:end + 1])


def identify_wine(image_bytes, mime_type="image/jpeg", api_key=None, model=None):
    api_key = api_key or os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    model = model or os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")
    data_url = "data:%s;base64,%s" % (mime_type, base64.b64encode(image_bytes).decode("ascii"))
    payload = {
        "model": model,
        "store": False,
        "input": [{
            "role": "user",
            "content": [
                {"type": "input_text", "text": SCHEMA_PROMPT},
                {"type": "input_image", "image_url": data_url, "detail": "high"}
            ]
        }]
    }
    req = urllib.request.Request(
        OPENAI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError("OpenAI API error %s: %s" % (exc.code, detail)) from exc
    text = body.get("output_text")
    if not text:
        chunks = []
        for item in body.get("output", []):
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    chunks.append(part.get("text", ""))
        text = "\n".join(chunks)
    result = _extract_json(text)
    result["confidence"] = max(0.0, min(1.0, float(result.get("confidence") or 0)))
    result["needs_confirmation"] = bool(result.get("needs_confirmation", True) or result["confidence"] < 0.85)
    result["source"] = "openai_vision"
    result["model"] = model
    return result
