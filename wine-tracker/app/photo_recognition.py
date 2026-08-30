"""Server-side wine photo recognition orchestration.

Keeps the browser free of provider secrets and only returns a candidate when
an actual image recognition provider produced one.
"""
from __future__ import annotations

from typing import Any

from providers.cork_dork_gemini import recognize_label


def recognize_wine_photo(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict[str, Any]:
    """Recognize a real uploaded wine photo and return a UI-safe result."""
    vision = recognize_label(image_bytes, mime_type)
    if vision.get("error"):
        return {"ok": False, "status": "not_recognized", "error": vision["error"]}

    producer = (vision.get("producer") or "").strip()
    wine_name = (vision.get("wine_name") or "").strip()
    if not producer and not wine_name:
        return {"ok": False, "status": "not_recognized"}

    confidence = vision.get("confidence")
    needs_confirmation = confidence is None or confidence < 0.92
    return {
        "ok": True,
        "status": "candidate",
        "candidate": {
            "producer": producer or None,
            "wine_name": wine_name or None,
            "vintage": vision.get("vintage"),
            "appellation": vision.get("appellation"),
            "region": vision.get("region"),
            "country": vision.get("country"),
            "grapes": vision.get("grapes"),
            "confidence": confidence,
            "visible_text": vision.get("visible_text"),
            "source": "photo_vision",
            "provider": vision.get("provider"),
            "model": vision.get("model"),
            "needs_confirmation": needs_confirmation,
        },
    }
