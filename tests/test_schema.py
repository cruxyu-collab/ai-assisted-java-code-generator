import pytest
from pydantic import ValidationError

from codegen.schema import DesignDefinition

VALID = {
    "class_name": "Customer",
    "fields": [
        {"name": "customerId", "type": "long", "required": True, "description": "顧客ID"},
        {"name": "customerName", "type": "String", "required": True, "description": "顧客名"},
    ],
}


def test_valid_design_is_accepted():
    design = DesignDefinition.model_validate(VALID)
    assert design.class_name == "Customer"
    assert len(design.fields) == 2


def test_missing_required_property_is_rejected():
    broken = {"class_name": "Customer", "fields": [{"name": "id", "type": "long", "required": True}]}
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(broken)


def test_duplicate_field_names_are_rejected():
    broken = {**VALID, "fields": [VALID["fields"][0], VALID["fields"][0]]}
    with pytest.raises(ValidationError, match="unique"):
        DesignDefinition.model_validate(broken)


def test_unsupported_type_is_rejected():
    broken = {**VALID, "fields": [{**VALID["fields"][0], "type": "BigDecimal"}]}
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(broken)


@pytest.mark.parametrize("bad_name", ["customer-name", "1customer", "class", "null"])
def test_invalid_or_reserved_field_names_are_rejected(bad_name):
    broken = {**VALID, "fields": [{**VALID["fields"][0], "name": bad_name}]}
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(broken)


def test_invalid_class_name_is_rejected():
    broken = {**VALID, "class_name": "customer-info"}
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(broken)


def test_empty_fields_are_rejected():
    broken = {**VALID, "fields": []}
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(broken)


def test_extra_properties_are_rejected():
    broken = {**VALID, "unexpected": "value"}
    with pytest.raises(ValidationError):
        DesignDefinition.model_validate(broken)
