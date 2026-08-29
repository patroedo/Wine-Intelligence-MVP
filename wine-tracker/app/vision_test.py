"""Local smoke test for wine label recognition.
Usage:
  OPENAI_API_KEY=... python vision_test.py /path/to/bottle.jpg
Windows PowerShell:
  $env:OPENAI_API_KEY='...'; python vision_test.py C:\\path\\bottle.jpg
"""
import json
import mimetypes
import sys
from openai_wine_vision import identify_wine

if len(sys.argv) != 2:
    raise SystemExit("Usage: python vision_test.py IMAGE_PATH")
path = sys.argv[1]
mime = mimetypes.guess_type(path)[0] or "image/jpeg"
with open(path, "rb") as f:
    image = f.read()
result = identify_wine(image, mime_type=mime)
print(json.dumps(result, ensure_ascii=False, indent=2))
