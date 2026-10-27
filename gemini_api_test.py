import os
from pathlib import Path
from google import genai
from google.genai import types

# 표준 라이브러리로 .env 파일 읽기
env_file = Path(".env")
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("[ERROR] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
    raise SystemExit(1)

print("[1] API 키 확인 완료 (앞 6자리):", api_key[:6] + "...", flush=True)

try:
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=15000)
    )
    print("[2] Gemini API 연결 요청 중 (모델: gemini-3.8-flash)...", flush=True)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with exactly: API_TEST_OK"
    )

    print("[3] API 응답 수신 성공!")
    print("응답 내용:", repr(response.text.strip()), flush=True)

except Exception as e:
    print("\n[FAIL] API 요청 실패:", type(e).__name__, flush=True)
    print("상세 오류:", str(e)[:1500], flush=True)
    raise SystemExit(1)