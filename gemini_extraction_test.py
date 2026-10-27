"""
gemini_extraction_test.py
基本設計書（Excel形式: .xlsx）の解析、Pydanticバリデーション、およびSelf-CorrectionループによるJavaコード生成実行スクリプト。
"""

import json
import os
import time
from pathlib import Path
from google import genai
from google.genai import types
from pydantic import ValidationError

from codegen.schema import DesignDefinition
from codegen.generator import render_java, write_java_file
from codegen.excel_reader import load_design_from_excel

# 1. 環境変数 (.env) の堅牢な読み込み (Windows BOM対応)
env_file = Path(".env")
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            k = key.strip()
            v = val.strip().strip('"').strip("'")
            if k:
                os.environ[k] = v

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("[ERROR] GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")

client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=60000))

# 2. 基本設計書Excelファイル（.xlsx）の読み込み（専用モジュール経由）
excel_file = Path("samples/customer_design.xlsx")
try:
    design_doc = load_design_from_excel(excel_file)
except Exception as e:
    raise SystemExit(f"[ERROR] Excel設計書読み込み失敗: {e}")

system_prompt = """
あなたは日本の業務システム開発におけるJava設計書解析アシスタントです。
以下の【設計書情報】（Excelシート抽出データ）を読み取り、クラス名および項目仕様を抽出して、指定されたJSONスキーマに厳密に準拠したJSONのみを出力してください。
Markdownのバッククォート(```)や説明文は一切含めないでください。

【JSONスキーマ要件】
- class_name: クラス名（PascalCase）
- fields: リスト形式
  - name: 項目変数名（lowerCamelCase）
  - type: Java型（"String", "int", "long", "boolean" のいずれか）
  - required: 必須フラグ（boolean: true または false）
  - description: 項目の日本語説明・論理名（文字列）
"""

# 3. Self-Correction（自律的自己修正）エージェントループ実行
MAX_RETRIES = 3
feedback = ""
validated_design = None

print(f"[Agent開始] 設計書Excel（{excel_file}）を読み込み、解析・自律生成ループを開始します...\n")

for attempt in range(1, MAX_RETRIES + 1):
    print(f"--- [試行回数 {attempt}/{MAX_RETRIES}] ---")
    current_prompt = f"{system_prompt}\n\n【設計書情報】\n{design_doc}"
    if feedback:
        current_prompt += f"\n\n【前回のバリデーションエラー - これを必ず修正してください】\n{feedback}"

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=current_prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0)
        )

        print("[Agent] LLMレスポンス受信完了。Pydanticによるデータ整合性検証中...")

        raw_data = json.loads(response.text)
        validated_design = DesignDefinition.model_validate(raw_data)
        print(">> [成功] Pydanticデータ整合性検証をパスしました。エージェントループを終了します。\n")
        break

    except (json.JSONDecodeError, ValidationError) as e:
        print(f">> [警告] 検証例外検知: {e}")
        feedback = str(e)
        if attempt == MAX_RETRIES:
            raise SystemExit("[Agent失敗] 最大再試行回数を超過しました。")

    except Exception as e:
        print(f">> [一時的通信例外検知 ({type(e).__name__})]: {e}")
        if attempt == MAX_RETRIES:
            raise SystemExit(f"[Agent失敗] API通信エラーにより終了: {e}")
        print(">> 2秒待機後に再試行します...")
        time.sleep(2)

# 4. 検証済みデータからのJavaソースファイル生成
output_path = write_java_file(validated_design, "output")
print(f"[完了] Javaソースファイル物理生成完了: {output_path.resolve()}")
print(render_java(validated_design))