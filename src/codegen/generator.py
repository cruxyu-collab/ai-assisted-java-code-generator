"""
src/codegen/generator.py
検証済みデータモデル（DesignDefinition）から標準Java DTOソースコードを決定論的に生成するモジュール。
JavaBeans仕様に準拠し、boolean型のアクセサには 'is' プレフィックスを適用。
"""

from pathlib import Path
from codegen.schema import DesignDefinition

# Java標準データ型マッピングテーブル（許可型ホワイトリスト）
JAVA_TYPES: dict[str, str] = {
    "String": "String",
    "int": "int",
    "long": "long",
    "boolean": "boolean"
}


def _safe_javadoc(value: str) -> str:
    """Javadoc構文破壊を防ぐためのエスケープ処理（閉じ記号および改行の無害化）。"""
    return value.replace("*/", "* /").replace("\r", " ").replace("\n", " ")


def render_java(design: DesignDefinition) -> str:
    """
    DesignDefinitionモデルを受け取り、完全なJava DTOソースコード文字列を生成。
    - 日本語論理名を含むJavadocコメントの自動付与
    - フィールドの完全カプセル化（private修飾子）
    - JavaBeans規格準拠アクセサ（boolean型は isActive()、その他は getXxx() / setXxx()）
    """
    lines = [
        "/** DTO generated from a validated design definition. */",
        f"public class {design.class_name} {{",
        "",
    ]
    # フィールド宣言
    for field in design.fields:
        lines.extend([
            f"    /** {_safe_javadoc(field.description)} */",
            f"    private {JAVA_TYPES[field.type]} {field.name};",
            "",
        ])
    # アクセサメソッド (Getter / Setter)
    for field in design.fields:
        java_type, name = JAVA_TYPES[field.type], field.name
        suffix = name[0].upper() + name[1:]
        
        # JavaBeans規約: boolean型は 'is'、その他は 'get'
        getter_prefix = "is" if field.type == "boolean" else "get"
        
        lines.extend([
            f"    public {java_type} {getter_prefix}{suffix}() {{",
            f"        return {name};",
            "    }",
            "",
            f"    public void set{suffix}({java_type} {name}) {{",
            f"        this.{name} = {name};",
            "    }",
            "",
        ])
    lines.append("}")
    return "\n".join(lines) + "\n"


def write_java_file(design: DesignDefinition, output_dir: str | Path) -> Path:
    """生成されたJavaコードを指定ディレクトリへ物理ファイルとして保存。"""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f"{design.class_name}.java"
    destination.write_text(render_java(design), encoding="utf-8", newline="\n")
    return destination