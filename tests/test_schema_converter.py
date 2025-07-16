"""Tests for schema converter utilities"""

import pytest


def test_get_python_type():
    """Test JSON Schema type to Python type conversion"""
    from opal_mcp_adapter.utils.schema_converter import _get_python_type

    assert _get_python_type({"type": "string"}) == str
    assert _get_python_type({"type": "integer"}) == int
    assert _get_python_type({"type": "number"}) == float
    assert _get_python_type({"type": "boolean"}) == bool
    assert _get_python_type({"type": "array"}) == list
    assert _get_python_type({"type": "object"}) == dict
    assert _get_python_type({}) == str  # Default to string


def test_json_schema_to_pydantic():
    """Test JSON Schema to Pydantic model conversion"""
    from opal_mcp_adapter.utils.schema_converter import json_schema_to_pydantic

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "active": {"type": "boolean"}
        },
        "required": ["name", "age"]
    }

    model_class = json_schema_to_pydantic(schema, "TestModel")

    # Test that the model can be instantiated
    instance = model_class(name="test", age=25)
    assert instance.name == "test"
    assert instance.age == 25
    assert instance.active is None  # Not required, should default to None


def test_parameter_descriptions_are_empty():
    """Test that all parameters have empty descriptions by default"""
    from opal_mcp_adapter.utils.schema_converter import json_schema_to_pydantic

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "User's full name"},
            "age": {"type": "integer", "description": "User's age"},
            "email": {"type": "string", "description": "User's email address"}
        },
        "required": ["name", "age"]
    }

    model_class = json_schema_to_pydantic(schema, "TestModel")

    # Check that all fields have empty descriptions
    for field_name in ["name", "age", "email"]:
        field = model_class.model_fields[field_name]
        assert field.description == "", (
            f"Field {field_name} should have empty description"
        )