# AI-Assisted Java Code Generator

[ 日本語 | [한국어](README.ko.md) ]

> **自然言語の基本設計書から、構文エラーゼロ・完全規約準拠のJavaデータ構造・ドメインモデルクラスを自律自動生成するバックエンド開発支援エンジン**  
> **防弾サニタイズ × Pydanticデータ契約 × 自律的修正（Self-Correction）ループ × 決定論的コード生成**

---

## 📌 概要 (Overview)

**AI-Assisted Java Code Generator** は、業務システム開発における基本設計書の記述揺れに伴う転記工数および人的ミスを根本から解消するために設計されたバックエンド開発支援エンジンです。

Excelやテキスト等で作成された非定型の基本設計書から、Google Gemini API を用いてクラス名およびフィールド仕様を高速抽出。**「4段階防弾サニタイズ層」**と**「Pydantic厳格データ契約層」**による多層防壁を通過させ、万一の抽出不整合時は例外詳細をプロンプトへ自己反映して自動再試行する **Self-Correction（自律的自己修正）エージェント機構** を内装しています。

検証済みのデータのみをパイプラインへ流し込み、Pythonのルールベースジェネレーターにより、コンパイル保証のある高品質なJavaデータ構造（DTO / VO / ドメインエンティティ骨格）コードを出力します。

```
[ システム特性 ]
• 責務分離設計: 意味解釈（LLM）と構文出力（Python生成器）を分離し、構文エラー発生率 0% を確立
• 防弾サニタイズ: Markdownフェンス・末尾カンマ・コメント混入を事前無害化する4段階正規表現前処理
• 自律的自己修正: バリデーション例外をプロンプトへ自己反映し最大3回再試行するエージェント機構
• 決定論的コード生成: 日本語Javadoc自動付与、完全カプセル化（private / Getter・Setter）準拠のJava 17+ POJO生成
• 高速品質保証: CI/CD環境およびローカルにおいて 20件の自動テストを 0.31秒 で全件パス
```

---

## 💡 解決する課題とアプローチ (Problem & Approach)

### 【課題】設計書転記に伴う人的ミスとAI直接生成の危険性
業務システムの基本設計書は現場によって記述形式が統一されておらず、手作業でのデータモデルクラス作成はタイポや型間違いの温床となります。一方、ChatGPT等の生成AIに直接Javaソースコード全体を出力させると、インデント不正、命名規約違反、存在しない型の捏造といったコンパイルエラーが不可避でした。

### 【アプローチ】二元論的分離と自律自己修正ループ
本システムは、「AIには意味解釈のみを任せ、コード生成は絶対確実なルールベースで行う」という厳格な役割分担を採用しています。
- **LLM構造化抽出**: 設計書テキストから項目論理名・物理名・型・必須フラグのみをJSONとして抽出。
- **データ契約検証**: Pydantic モデルにより、Java識別子規約および許可されたデータ型を厳格検査。
- **Self-Correctionループ**: 抽出データに不整合があれば、バリデーション例外をLLMに自動再注入して自律修正。
- **決定論的レンダリング**: 検証を完全に通過したデータのみを、純粋なPythonロジックで標準Javaコードへ書き出し。

---

## 🛠 技術的工夫と設計詳細 (Engineering Highlights)

### 1. 防弾JSONサニタイズパイプライン (Bulletproof Sanitization)
LLMの出力には、Markdownコードブロック（````json ... ````）やインラインコメント、末尾カンマが混入するリスクが常に存在します。パーサーの前段に以下の4段階正規表現前処理を配置し、構文破壊を100%防止しています：
1. **境界抽出**: 最も外側の `{` から `}` までを切り出し、前後の不要テキストを強制排除。
2. **コメント除去**: `// ...` 形式のインラインコメントを空文字に置換。
3. **末尾カンマ置換**: 閉じ括弧直前の余分なカンマを自動切除。
4. **未クォートキー補正**: `key:` 形式の不正キーを `"key":` に自動修正。

### 2. Pydanticデータ契約と自律修正（Self-Correction）エージェント
抽出結果は即時に `DesignDefinition` モデルによって型検査を受けます。
- クラス名（PascalCase）および変数名（lowerCamelCase）、Java言語予約語の検査。
- 許可されたJava型（`String`, `int`, `long`, `boolean`）のホワイトリスト厳格制限。
- バリデーション失敗時は、発生した `ValidationError` の具体的内容（欠落項目・不正型）をプロンプトへ追加し自動再試行（最大3回）。

### 3. Javadoc付与と完全カプセル化（POJO）の決定論的出力
設計書の日本語論理名を反映したJavadocコメントを各フィールドおよびアクセサメソッドに自動付与します。外部ライブラリに依存しない標準的なJavaコードを物理ファイル（`output/Customer.java`）として出力するため、既存のあらゆるエンタープライズビルド環境（Maven / Gradle）に即座に組み込み可能です。

---

## 🔒 データガバナンスとセキュリティ

- **ローカル処理原則**: 入力された設計書データおよび生成されたJavaソースコードはすべてローカル環境内で処理され、外部DBへの保存は行いません。
- **エフェメラルAPI通信**: 構造化抽出時のみGoogle Gemini APIへHTTPS通信を行い、推論完了後のテキストデータは破棄されます。
- **秘匿情報管理**: APIキーは環境変数（`.env`）で管理し、コードベース内へのハードコーディングを完全に防止しています。

---

## 💻 技術スタック (Tech Stack)

```
[ 実行基盤 & データ検証 ]
• Python 3.14.8 (Core Engine)
• Pydantic v2.10+ (Data Contract & Type Safety)
• pytest / anyio (Automated Test Suite)

[ AI推論エンジン ]
• Google Gemini API (gemini-3.8-flash)
• Structured Output (responseMimeType: application/json, temperature: 0)
• Self-Correction Agent Loop (Max Retries: 3)

[ 生成対象仕様 ]
• Java SE 17+ (Standard Data Structure / Domain Model Specification)
• Fully Encapsulated (Private Fields, Standard Accessors, Japanese Javadoc)
```

---

## 🧪 品質検証実績 (Quality Assurance)

CI/CDおよびローカル環境において、異常系・境界値・サニタイズを含む全20件のテストケースを**0.31秒で100%全パス**しています。

```bash
$ pytest -v
============================= test session starts =============================
tests/test_ai_validation_defense.py ...                                  [ 15%]
tests/test_generator.py ...                                              [ 30%]
tests/test_schema.py ...........                                         [ 85%]
tests/test_validator.py ...                                              [100%]

============================= 20 passed in 0.31s ==============================
```

---

## 📂 実機検証・入出力サンプル (Input & Output Showcase)

本リポジトリでは、実際の非定型基本設計書（Wiki/Markdown仕様書）から完全なJavaモデルクラスが出力される一連の変換結果をそのまま確認可能です：

- 📄 **[入力: 基本設計書仕様 (samples/customer_design.md)](samples/customer_design.md)**
- ☕ **[出力: 生成されたJavaモデルクラス (output/Customer.java)](output/Customer.java)**

---

## 📚 技術詳細ドキュメント

- 📐 **[アーキテクチャ設計決定記録 (docs/ja/DECISIONS.md)](docs/ja/DECISIONS.md)**
- 📋 **[要件定義仕様書 (docs/ja/REQUIREMENTS.md)](docs/ja/REQUIREMENTS.md)**
- 📊 **[品質検証およびテスト実績報告書 (docs/ja/TEST_RESULTS.md)](docs/ja/TEST_RESULTS.md)**
- 📈 **[プロジェクト進捗実績報告書 (docs/ja/PROJECT_STATUS.md)](docs/ja/PROJECT_STATUS.md)**
- 🤝 **[システム運用・開発引き継ぎ仕様書 (docs/ja/HANDOFF.md)](docs/ja/HANDOFF.md)**