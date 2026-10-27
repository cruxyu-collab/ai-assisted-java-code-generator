"""
tests/test_generator.py
Java DTOコード生成器（generator.py）の構文・Javadoc・JavaBeans規約・ファイル出力検証テスト。
"""

from pathlib import Path
import pytest
from codegen.generator import render_java, write_java_file, _safe_javadoc
from codegen.schema import DesignDefinition


def test_safe_javadoc():
    """Javadocコメント内のエスケープ処理（閉じ記号および改行置換）が正しく行われるかを検証。"""
    assert _safe_javadoc("test*/comment") == "test* /comment"
    assert _safe_javadoc("line1\nline2\rline3") == "line1 line2 line3"


def test_render_java_dto_and_javabeans_naming():
    """
    DesignDefinitionモデルから規約に準拠したJavaソースが生成されるかを検証。
    JavaBeans規約に則り、boolean型は isActive()、通常型は getCustomerId() となることを検証。
    """
    data = {
        "class_name": "Customer",
        "fields": [
            {"name": "customerId", "type": "long", "required": True, "description": "顧客ID"},
            {"name": "customerName", "type": "String", "required": True, "description": "顧客名"},
            {"name": "active", "type": "boolean", "required": True, "description": "有効フラグ"},
        ],
    }
    design = DesignDefinition.model_validate(data)
    code = render_java(design)

    # クラス定義
    assert "public class Customer {" in code

    # long型: getCustomerId()
    assert "private long customerId;" in code
    assert "public long getCustomerId() {" in code
    assert "public void setCustomerId(long customerId) {" in code

    # String型: getCustomerName()
    assert "private String customerName;" in code
    assert "public String getCustomerName() {" in code
    assert "public void setCustomerName(String customerName) {" in code

    # boolean型 (JavaBeans規格): isActive()
    assert "private boolean active;" in code
    assert "public boolean isActive() {" in code
    assert "public void setActive(boolean active) {" in code


def test_write_java_file(tmp_path: Path):
    """指定ディレクトリへ完全なJavaソースが実ファイルとして物理保存されるかを検証。"""
    data = {
        "class_name": "Product",
        "fields": [
            {"name": "productId", "type": "int", "required": True, "description": "商品ID"},
        ],
    }
    design = DesignDefinition.model_validate(data)
    output_file = write_java_file(design, tmp_path)

    assert output_file.exists()
    assert output_file.name == "Product.java"
    content = output_file.read_text(encoding="utf-8")
    assert "public class Product {" in content