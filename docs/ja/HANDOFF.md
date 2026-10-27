# システム運用・開発引き継ぎ仕様書 (System Handover & Operations Guide)

本ドキュメントは、AI-Assisted Java Code Generatorの後続開発者および運用担当エンジニアに向けた、開発環境の再現、アーキテクチャ運用、およびトラブルシューティングに関する公式引き継ぎ仕様書です。

---

## 1. システム概要および運用目的

- **システム名称**: AI-Assisted Java Code Generator (AI-Assisted Java Code Generator)
- **コア機能**: 自然言語設計書の構造化抽出、Pydanticデータ整合性検証、決定論的Java DTOソース自動出力
- **設計思想**:
  - LLMの役割を「意味解釈」に限定し、ソース構文出力はPythonテンプレートジェネレーターへ完全委譲。
  - バリデーション失敗時はプロンプトへ例外を自己反映する Self-Correction エージェント機構を内装。

---

## 2. 開発・実行環境の再現手順 (Environment Setup)

Windows 10/11 環境下で本システムを運用・再構築するための標準手順です。

```powershell
# 1. 仮想環境の作成および有効化
py -3.14 -m venv .venv
.\.venv\Scripts\activate

# 2. 必須パッケージの依存関係解決
pip install --upgrade pip
pip install google-genai pydantic pytest python-pptx

# 3. 環境変数ファイルの配置
# プロジェクトルートに .env を作成し、以下を定義
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 3. 日常運用および検証コマンド (Operations Cheat Sheet)

```powershell
# ① 全自動テストスイートの実行 (回帰テスト: 20件が全パスすることを確認)
python -m pytest -v

# ② AI連携コード生成パイプラインの単体実行
python gemini_extraction_test.py
# (生成物: output/Customer.java が出力されることを確認)

# ③ ローカル仕様書JSONの単独検証
python -m codegen.validator samples\customer.json

# ④ システムアーキテクチャ解説用スライド (PPTX) の自動再生成
python make_presentation.py
```

---

## 4. アーキテクチャ境界および保守上の留意点

1. **データ契約の保守 (`src/codegen/schema.py`)**:
   - `DesignDefinition` で許可されているJava型は現在 `String`, `int`, `long`, `boolean` の4種に限定されています。
   - 今後 `BigDecimal` や `LocalDate` を追加する場合は、`schema.py` の型ホワイトリストおよび `generator.py` のインポート文生成ロジックの双方を同期更新してください。

2. **AIモデル設定の保守 (`gemini_extraction_test.py`)**:
   - 推論モデルは `gemini-3.8-flash` を指定し、`temperature: 0`、`responseMimeType: "application/json"` を維持してください。
   - API過負荷やタイムアウト発生時は、`src/codegen/ai_extractor.py` のサニタイズパイプラインを経由していることを確認してください。

3. **セキュリティガバナンス**:
   - APIキーは絶対にソースコード内へ直接書き込まず、`.env` 経由でのみ参照してください。
   - 入力設計書データは推論終了後、ローカルメモリ上で即時破棄され、外部サーバーへ永続化されません。
