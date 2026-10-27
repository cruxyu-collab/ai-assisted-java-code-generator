"""Pydantic models for structured design data."""
from typing import Literal
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

JavaType = Literal["String", "int", "long", "boolean"]

JAVA_KEYWORDS = {
    "abstract", "assert", "boolean", "break", "byte", "case", "catch",
    "char", "class", "const", "continue", "default", "do", "double",
    "else", "enum", "extends", "final", "finally", "float", "for",
    "goto", "if", "implements", "import", "instanceof", "int", "interface",
    "long", "native", "new", "package", "private", "protected", "public",
    "return", "short", "static", "strictfp", "super", "switch",
    "synchronized", "this", "throw", "throws", "transient", "try", "void",
    "volatile", "while", "true", "false", "null", "_",
}
JAVA_IDENTIFIER = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


def validate_java_identifier(value: str) -> str:
    if not JAVA_IDENTIFIER.fullmatch(value):
        raise ValueError("must be a valid Java identifier (ASCII subset)")
    if value in JAVA_KEYWORDS:
        raise ValueError("must not be a Java keyword or reserved literal")
    return value


class FieldDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1)
    type: JavaType
    required: bool
    description: str = Field(min_length=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return validate_java_identifier(value)


class DesignDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    class_name: str = Field(min_length=1)
    fields: list[FieldDefinition] = Field(min_length=1)

    @field_validator("class_name")
    @classmethod
    def validate_class_name(cls, value: str) -> str:
        return validate_java_identifier(value)

    @model_validator(mode="after")
    def ensure_unique_field_names(self):
        names = [item.name for item in self.fields]
        if len(names) != len(set(names)):
            raise ValueError("field names must be unique")
        return self
