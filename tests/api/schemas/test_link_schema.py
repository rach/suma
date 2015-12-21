from suma.api.schemas import LinkSchema
from schematics.exceptions import ModelValidationError, ModelConversionError
import pytest


def test_valid_link_schema():
    schema = LinkSchema({"url": "https://google.com"})
    schema.validate()
    assert schema.url == "https://google.com"
    assert schema.user_id is None


def test_link_schema_url_required():
    schema = LinkSchema({})
    with pytest.raises(ModelValidationError) as excinfo:
        schema.validate()
    assert 'url' in str(excinfo.value)


def test_valid_link_schema_with_user_id():
    schema = LinkSchema({"url": "https://google.com", "user_id": 1})
    schema.validate()
    assert schema.url == "https://google.com"
    assert schema.user_id == 1


def test_link_schema_with_invalid_url():
    schema = LinkSchema({"url": "fail", "user_id": 1L})
    with pytest.raises(ModelValidationError) as excinfo:
        schema.validate()
    assert 'url' in str(excinfo.value)


def test_link_schema_with_invalid_user_id():
    with pytest.raises(ModelConversionError) as excinfo:
        schema = LinkSchema({"url": "https://google.com", "user_id": "fail"})
        schema.validate()
    assert 'user_id' in str(excinfo.value)
