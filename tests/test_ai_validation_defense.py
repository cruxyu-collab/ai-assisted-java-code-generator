"""
tests/test_ai_validation_defense.py
LLMの異常系レスポンス（ハルシネーション・フォーマット不正）に対するPydantic防壁検証テスト。
"""

import pytest
from pydantic import ValidationError
from codegen.schema import DesignDefinition


def test_ai_output_missing_class_name():
    """LLMがクラス名を欠落させて出力した場合、Pydanticが検知して遮断することを検証。"""
    bad_ai_output = {
        "fields": [
            {"name": "id", "type": "long", "required": True, "description": "ID"}
        ]
    }
    with pytest.raises(ValidationError) as exc_info:
        DesignDefinition.model_validate(bad_ai_output)
    assert "class_name" in str(exc_info.value)


def test_ai_output_unsupported_java_type():
    """LLMが未定義の不正なJava型を出力した場合、ホワイトリスト検査で拒絶することを検証。"""
    bad_ai_output = {
        "class_name": "TestDto",
        "fields": [
            {"name": "createdDate", "type": "datetime_invalid", "required": True, "description": "作成日時"}
        ]
    }
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(bad_ai_output)


def test_ai_output_empty_fields():
    """LLMがフィールドリストを空配列で返却した場合、フェイルセーフとして遮断することを検証。"""
    bad_ai_output = {
        "class_name": "EmptyDto",
        "fields": []
    }
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(bad_ai_output)