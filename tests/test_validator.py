import json
import pytest

from codegen.validator import load_and_validate


def test_loads_sample_json(tmp_path):
    sample = {
        "class_name": "Customer",
        "fields": [
            {"name": "id", "type": "long", "required": True, "description": "顧客ID"}
        ],
    }
    path = tmp_path / "sample.json"
    path.write_text(json.dumps(sample, ensure_ascii=False), encoding="utf-8")
    assert load_and_validate(path).class_name == "Customer"


def test_invalid_json_reports_error(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_and_validate(path)


def test_non_object_json_is_rejected(tmp_path):
    path = tmp_path / "array.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="object"):
        load_and_validate(path)
