"""Unit tests for domain validators."""

import pytest

from form_filler.domain.exceptions import DataValidationError, FieldMappingError, ValidationError
from form_filler.domain.validators import (
    validate_field_mapping,
    validate_field_value,
    validate_user_data,
)
from form_filler.domain.value_objects import FieldType


class TestValidateFieldValue:
    """Test the validate_field_value function."""

    # TEXT field tests
    def test_validate_text_field_with_string(self):
        """Test TEXT field validation with string value."""
        result = validate_field_value("John Doe", FieldType.TEXT, "name")
        assert result == "John Doe"

    def test_validate_text_field_with_number(self):
        """Test TEXT field validation converts number to string."""
        result = validate_field_value(42, FieldType.TEXT, "id")
        assert result == "42"

    def test_validate_text_field_required_empty(self):
        """Test TEXT field validation fails when required and empty."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value("", FieldType.TEXT, "name", required=True)
        assert "Required field 'name' cannot be empty" in str(exc_info.value)

    def test_validate_text_field_not_required_empty(self):
        """Test TEXT field validation allows empty when not required."""
        result = validate_field_value("", FieldType.TEXT, "nickname", required=False)
        assert result == ""

    # BOOLEAN field tests
    def test_validate_boolean_field_with_bool(self):
        """Test BOOLEAN field validation with boolean value."""
        assert validate_field_value(True, FieldType.BOOLEAN, "active") is True
        assert validate_field_value(False, FieldType.BOOLEAN, "active") is False

    def test_validate_boolean_field_with_string_true(self):
        """Test BOOLEAN field validation with truthy strings."""
        assert validate_field_value("true", FieldType.BOOLEAN, "flag") is True
        assert validate_field_value("yes", FieldType.BOOLEAN, "flag") is True
        assert validate_field_value("1", FieldType.BOOLEAN, "flag") is True
        assert validate_field_value("on", FieldType.BOOLEAN, "flag") is True

    def test_validate_boolean_field_with_string_false(self):
        """Test BOOLEAN field validation with falsy strings."""
        assert validate_field_value("false", FieldType.BOOLEAN, "flag") is False
        assert validate_field_value("no", FieldType.BOOLEAN, "flag") is False
        assert validate_field_value("0", FieldType.BOOLEAN, "flag") is False
        assert validate_field_value("off", FieldType.BOOLEAN, "flag") is False

    def test_validate_boolean_field_with_number(self):
        """Test BOOLEAN field validation with numeric values."""
        assert validate_field_value(1, FieldType.BOOLEAN, "flag") is True
        assert validate_field_value(0, FieldType.BOOLEAN, "flag") is False
        assert validate_field_value(42, FieldType.BOOLEAN, "flag") is True

    def test_validate_boolean_field_invalid_string(self):
        """Test BOOLEAN field validation fails with invalid string."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value("maybe", FieldType.BOOLEAN, "flag")
        assert "Cannot convert string 'maybe' to boolean" in str(exc_info.value)

    # NUMBER field tests
    def test_validate_number_field_with_int(self):
        """Test NUMBER field validation with integer."""
        result = validate_field_value(42, FieldType.NUMBER, "age")
        assert result == 42.0
        assert isinstance(result, float)

    def test_validate_number_field_with_float(self):
        """Test NUMBER field validation with float."""
        result = validate_field_value(3.14, FieldType.NUMBER, "pi")
        assert result == 3.14

    def test_validate_number_field_with_string(self):
        """Test NUMBER field validation with numeric string."""
        result = validate_field_value("123", FieldType.NUMBER, "count")
        assert result == 123.0

    def test_validate_number_field_with_formatted_string(self):
        """Test NUMBER field validation with formatted numeric string."""
        result = validate_field_value("1,234.56", FieldType.NUMBER, "amount")
        assert result == 1234.56

    def test_validate_number_field_invalid_string(self):
        """Test NUMBER field validation fails with non-numeric string."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value("abc", FieldType.NUMBER, "count")
        assert "Cannot convert string 'abc' to number" in str(exc_info.value)

    def test_validate_number_field_with_min_value(self):
        """Test NUMBER field validation with minimum value constraint."""
        result = validate_field_value(25, FieldType.NUMBER, "age", min_value=18)
        assert result == 25.0

    def test_validate_number_field_below_min_value(self):
        """Test NUMBER field validation fails below minimum."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value(15, FieldType.NUMBER, "age", min_value=18)
        assert "below minimum" in str(exc_info.value)

    def test_validate_number_field_with_max_value(self):
        """Test NUMBER field validation with maximum value constraint."""
        result = validate_field_value(100, FieldType.NUMBER, "score", max_value=150)
        assert result == 100.0

    def test_validate_number_field_above_max_value(self):
        """Test NUMBER field validation fails above maximum."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value(200, FieldType.NUMBER, "score", max_value=150)
        assert "exceeds maximum" in str(exc_info.value)

    def test_validate_number_field_within_range(self):
        """Test NUMBER field validation with both min and max constraints."""
        result = validate_field_value(
            50, FieldType.NUMBER, "percentage", min_value=0, max_value=100
        )
        assert result == 50.0

    # DATE field tests
    def test_validate_date_field_with_string(self):
        """Test DATE field validation with string."""
        result = validate_field_value("2025-01-15", FieldType.DATE, "birth_date")
        assert result == "2025-01-15"

    def test_validate_date_field_empty_not_required(self):
        """Test DATE field validation allows empty when not required."""
        result = validate_field_value("", FieldType.DATE, "birth_date", required=False)
        assert result == ""

    def test_validate_date_field_empty_required(self):
        """Test DATE field validation fails when empty and required."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value("", FieldType.DATE, "birth_date", required=True)
        assert "Required field 'birth_date' cannot be empty" in str(exc_info.value)

    # CHOICE/DROPDOWN/RADIO field tests
    def test_validate_choice_field_with_valid_option(self):
        """Test CHOICE field validation with valid option."""
        result = validate_field_value(
            "Option1",
            FieldType.CHOICE,
            "color",
            options=["Option1", "Option2", "Option3"],
        )
        assert result == "Option1"

    def test_validate_choice_field_invalid_option(self):
        """Test CHOICE field validation fails with invalid option."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value(
                "Invalid",
                FieldType.CHOICE,
                "color",
                options=["Option1", "Option2"],
            )
        assert "not in allowed options" in str(exc_info.value)

    def test_validate_choice_field_no_options(self):
        """Test CHOICE field validation without options list."""
        result = validate_field_value("AnyValue", FieldType.CHOICE, "selection")
        assert result == "AnyValue"

    def test_validate_dropdown_field(self):
        """Test DROPDOWN field validation."""
        result = validate_field_value(
            "Item1",
            FieldType.DROPDOWN,
            "menu",
            options=["Item1", "Item2"],
        )
        assert result == "Item1"

    def test_validate_radio_field(self):
        """Test RADIO field validation."""
        result = validate_field_value(
            "Choice1",
            FieldType.RADIO,
            "selection",
            options=["Choice1", "Choice2"],
        )
        assert result == "Choice1"

    # CHECKBOX field tests
    def test_validate_checkbox_field(self):
        """Test CHECKBOX field validation (similar to BOOLEAN)."""
        assert validate_field_value(True, FieldType.CHECKBOX, "agree") is True
        assert validate_field_value("yes", FieldType.CHECKBOX, "agree") is True

    # UNKNOWN field tests
    def test_validate_unknown_field_type(self):
        """Test validation of UNKNOWN field type returns value as-is."""
        result = validate_field_value("anything", FieldType.UNKNOWN, "mystery")
        assert result == "anything"

    # Required field tests
    def test_validate_required_field_with_none(self):
        """Test required field validation fails with None."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value(None, FieldType.TEXT, "name", required=True)
        assert "Required field 'name' cannot be empty" in str(exc_info.value)

    def test_validate_not_required_field_with_none(self):
        """Test non-required field validation allows None."""
        result = validate_field_value(None, FieldType.TEXT, "nickname", required=False)
        assert result is None


class TestValidateUserData:
    """Test the validate_user_data function."""

    def test_validate_simple_user_data(self):
        """Test validation of simple user data."""
        data = {"name": "Alice", "age": 30}
        result = validate_user_data(data)
        assert result == data

    def test_validate_empty_user_data(self):
        """Test validation of empty user data."""
        result = validate_user_data({})
        assert result == {}

    def test_validate_empty_user_data_with_required_fields(self):
        """Test validation fails for empty data with required fields."""
        with pytest.raises(DataValidationError) as exc_info:
            validate_user_data({}, required_fields=["name"])
        assert "User data is empty but required fields are specified" in str(exc_info.value)

    def test_validate_user_data_not_dict(self):
        """Test validation fails when user_data is not a dictionary."""
        with pytest.raises(ValidationError) as exc_info:
            validate_user_data("not a dict")  # type: ignore
        assert "User data must be a dictionary" in str(exc_info.value)

    def test_validate_user_data_with_required_fields_present(self):
        """Test validation passes when all required fields present."""
        data = {"name": "Bob", "email": "bob@example.com", "age": 25}
        result = validate_user_data(data, required_fields=["name", "email"])
        assert result == data

    def test_validate_user_data_with_missing_required_fields(self):
        """Test validation fails when required fields are missing."""
        data = {"name": "Charlie"}
        with pytest.raises(DataValidationError) as exc_info:
            validate_user_data(data, required_fields=["name", "email", "phone"])
        assert "Missing required fields" in str(exc_info.value)
        assert "email" in str(exc_info.value)
        assert "phone" in str(exc_info.value)

    def test_validate_user_data_with_field_types(self):
        """Test validation with field type checking."""
        data = {"name": "Dave", "age": 30, "active": True}
        field_types = {
            "name": FieldType.TEXT,
            "age": FieldType.NUMBER,
            "active": FieldType.BOOLEAN,
        }
        result = validate_user_data(data, field_types=field_types)
        assert result == data

    def test_validate_user_data_with_invalid_field_type(self):
        """Test validation fails with invalid field type."""
        data = {"age": "not a number"}
        field_types = {"age": FieldType.NUMBER}
        with pytest.raises(DataValidationError) as exc_info:
            validate_user_data(data, field_types=field_types)
        assert "Invalid value for field 'age'" in str(exc_info.value)

    def test_validate_user_data_with_required_and_types(self):
        """Test validation with both required fields and type checking."""
        data = {"name": "Eve", "age": 28}
        result = validate_user_data(
            data,
            required_fields=["name"],
            field_types={"age": FieldType.NUMBER},
        )
        assert result == data

    def test_validate_user_data_partial_field_types(self):
        """Test validation with field types for only some fields."""
        data = {"name": "Frank", "age": 35, "nickname": "Frankie"}
        field_types = {"age": FieldType.NUMBER}  # Only validate age
        result = validate_user_data(data, field_types=field_types)
        assert result == data


class TestValidateFieldMapping:
    """Test the validate_field_mapping function."""

    def test_validate_simple_field_mapping(self):
        """Test validation of simple field mapping."""
        user_field, form_field, confidence = validate_field_mapping(
            "first_name",
            "firstName",
        )
        assert user_field == "first_name"
        assert form_field == "firstName"
        assert confidence == 1.0

    def test_validate_field_mapping_with_confidence(self):
        """Test validation of field mapping with custom confidence."""
        user_field, form_field, confidence = validate_field_mapping(
            "name",
            "full_name",
            confidence=0.85,
        )
        assert user_field == "name"
        assert form_field == "full_name"
        assert confidence == 0.85

    def test_validate_field_mapping_empty_user_field(self):
        """Test validation fails with empty user field."""
        with pytest.raises(ValidationError) as exc_info:
            validate_field_mapping("", "form_field")
        assert "user_field must be a non-empty string" in str(exc_info.value)

    def test_validate_field_mapping_empty_form_field(self):
        """Test validation fails with empty form field."""
        with pytest.raises(ValidationError) as exc_info:
            validate_field_mapping("user_field", "")
        assert "form_field must be a non-empty string" in str(exc_info.value)

    def test_validate_field_mapping_invalid_user_field_type(self):
        """Test validation fails with non-string user field."""
        with pytest.raises(ValidationError) as exc_info:
            validate_field_mapping(123, "form_field")  # type: ignore
        assert "user_field must be a non-empty string" in str(exc_info.value)

    def test_validate_field_mapping_invalid_form_field_type(self):
        """Test validation fails with non-string form field."""
        with pytest.raises(ValidationError) as exc_info:
            validate_field_mapping("user_field", None)  # type: ignore
        assert "form_field must be a non-empty string" in str(exc_info.value)

    def test_validate_field_mapping_confidence_too_low(self):
        """Test validation fails with confidence below 0.0."""
        with pytest.raises(FieldMappingError) as exc_info:
            validate_field_mapping("user_field", "form_field", confidence=-0.1)
        assert "Confidence score must be between 0.0 and 1.0" in str(exc_info.value)

    def test_validate_field_mapping_confidence_too_high(self):
        """Test validation fails with confidence above 1.0."""
        with pytest.raises(FieldMappingError) as exc_info:
            validate_field_mapping("user_field", "form_field", confidence=1.5)
        assert "Confidence score must be between 0.0 and 1.0" in str(exc_info.value)

    def test_validate_field_mapping_invalid_confidence_type(self):
        """Test validation fails with non-numeric confidence."""
        with pytest.raises(ValidationError) as exc_info:
            validate_field_mapping("user_field", "form_field", confidence="high")  # type: ignore
        assert "confidence must be a number" in str(exc_info.value)

    def test_validate_field_mapping_with_user_data(self):
        """Test validation with user data verification."""
        user_data = {"email": "test@example.com", "phone": "123-456-7890"}
        user_field, form_field, confidence = validate_field_mapping(
            "email",
            "email_address",
            user_data=user_data,
        )
        assert user_field == "email"
        assert form_field == "email_address"

    def test_validate_field_mapping_user_field_not_in_data(self):
        """Test validation fails when user field not in user data."""
        user_data = {"email": "test@example.com"}
        with pytest.raises(FieldMappingError) as exc_info:
            validate_field_mapping(
                "phone",
                "phone_number",
                user_data=user_data,
            )
        assert "User field 'phone' not found in user data" in str(exc_info.value)

    def test_validate_field_mapping_invalid_user_data_type(self):
        """Test validation fails when user_data is not a dict."""
        with pytest.raises(ValidationError) as exc_info:
            validate_field_mapping(
                "field1",
                "field2",
                user_data="not a dict",  # type: ignore
            )
        assert "user_data must be a dictionary" in str(exc_info.value)

    def test_validate_field_mapping_with_form_fields(self):
        """Test validation with form fields verification."""
        form_fields = ["firstName", "lastName", "email"]
        user_field, form_field, confidence = validate_field_mapping(
            "first_name",
            "firstName",
            form_fields=form_fields,
        )
        assert user_field == "first_name"
        assert form_field == "firstName"

    def test_validate_field_mapping_form_field_not_in_list(self):
        """Test validation fails when form field not in form fields list."""
        form_fields = ["firstName", "lastName"]
        with pytest.raises(FieldMappingError) as exc_info:
            validate_field_mapping(
                "email",
                "email_address",
                form_fields=form_fields,
            )
        assert "Form field 'email_address' not found in form fields" in str(exc_info.value)

    def test_validate_field_mapping_invalid_form_fields_type(self):
        """Test validation fails when form_fields is not a list."""
        with pytest.raises(ValidationError) as exc_info:
            validate_field_mapping(
                "field1",
                "field2",
                form_fields="not a list",  # type: ignore
            )
        assert "form_fields must be a list" in str(exc_info.value)

    def test_validate_field_mapping_with_all_options(self):
        """Test validation with all optional parameters."""
        user_data = {"name": "Alice", "age": 30}
        form_fields = ["full_name", "user_age", "email"]

        user_field, form_field, confidence = validate_field_mapping(
            "name",
            "full_name",
            confidence=0.9,
            user_data=user_data,
            form_fields=form_fields,
        )

        assert user_field == "name"
        assert form_field == "full_name"
        assert confidence == 0.9


class TestValidatorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_validate_field_value_with_whitespace(self):
        """Test field value validation with whitespace."""
        # Leading/trailing whitespace in text should be preserved
        result = validate_field_value("  Alice  ", FieldType.TEXT, "name")
        assert result == "  Alice  "

        # Empty string with whitespace is still empty
        with pytest.raises(DataValidationError):
            validate_field_value("   ", FieldType.TEXT, "name", required=True)

    def test_validate_number_with_zero(self):
        """Test number validation with zero value."""
        result = validate_field_value(0, FieldType.NUMBER, "count")
        assert result == 0.0

    def test_validate_number_with_negative(self):
        """Test number validation with negative value."""
        result = validate_field_value(-42, FieldType.NUMBER, "balance")
        assert result == -42.0

    def test_validate_boolean_case_insensitive(self):
        """Test boolean validation is case-insensitive."""
        assert validate_field_value("TRUE", FieldType.BOOLEAN, "flag") is True
        assert validate_field_value("False", FieldType.BOOLEAN, "flag") is False
        assert validate_field_value("YES", FieldType.BOOLEAN, "flag") is True

    def test_validate_boolean_empty_string_not_required(self):
        """Test boolean validation with empty string when not required."""
        result = validate_field_value("", FieldType.BOOLEAN, "flag", required=False)
        assert result == ""  # Empty string returns as-is when not required

    def test_validate_empty_options_list(self):
        """Test choice validation with empty options list."""
        # Empty list means no valid options
        with pytest.raises(DataValidationError):
            validate_field_value("anything", FieldType.CHOICE, "field", options=[])

    def test_validate_field_value_with_list_value(self):
        """Test validation handles list values that can be converted to string."""
        # For TEXT type, lists should be converted to string
        result = validate_field_value([1, 2, 3], FieldType.TEXT, "items")
        assert result == "[1, 2, 3]"

    def test_validate_date_field_with_non_string(self):
        """Test DATE field validation with non-string convertible value."""
        # Date should convert non-string to string
        result = validate_field_value(20250115, FieldType.DATE, "date")
        assert result == "20250115"

    def test_validate_choice_field_converts_to_string(self):
        """Test CHOICE field validation converts non-string to string."""
        result = validate_field_value(123, FieldType.CHOICE, "option")
        assert result == "123"

    def test_validate_number_field_with_invalid_type(self):
        """Test NUMBER field validation with completely invalid type."""
        # Use a dict which won't convert to number
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value({"key": "value"}, FieldType.NUMBER, "count")
        assert "Cannot convert" in str(exc_info.value)

    def test_validate_boolean_with_invalid_type(self):
        """Test BOOLEAN field validation with invalid type."""
        # Use a dict which won't convert to boolean
        with pytest.raises(DataValidationError) as exc_info:
            validate_field_value({"key": "value"}, FieldType.BOOLEAN, "flag")
        assert "Cannot convert" in str(exc_info.value)
