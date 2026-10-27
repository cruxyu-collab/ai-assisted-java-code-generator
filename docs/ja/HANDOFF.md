# システム運用・開発引き継ぎ仕様書 (System Handover Guide)

---

## 1. 開発環境の再現手順
```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install google-genai pydantic pytest python-pptx openpyxl
```

## 2. 日常検証コマンド
```powershell
# 自動テストスイート実行 (20件 0.43秒全件パス)
python -m pytest -v

# AI連携コード生成パイプライン実行 (Excel入力 ➔ Java生成)
python gemini_extraction_test.py
```
