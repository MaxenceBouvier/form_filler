"""Unit tests for domain value objects."""

import pytest

from form_filler.domain.exceptions import ValidationError
from form_filler.domain.value_objects import FieldCategory, FieldType, FieldValue, FilePath


class TestFieldType:
    """Test the FieldType enum value object."""

    def test_field_type_values(self):
        """Test that FieldType enum has all required values."""
        assert FieldType.TEXT.value == "text"
        assert FieldType.BOOLEAN.value == "boolean"
        assert FieldType.DATE.value == "date"
        assert FieldType.NUMBER.value == "number"
        assert FieldType.CHECKBOX.value == "checkbox"
        assert FieldType.RADIO.value == "radio"
        assert FieldType.DROPDOWN.value == "dropdown"

    def test_field_type_immutable(self):
        """Test that FieldType enum values are immutable."""
        field_type = FieldType.TEXT
        with pytest.raises(AttributeError):
            field_type.value = "modified"  # type: ignore

    def test_field_type_equality(self):
        """Test equality comparison between FieldType values."""
        assert FieldType.TEXT == FieldType.TEXT
        assert FieldType.TEXT != FieldType.BOOLEAN  # type: ignore[comparison-overlap]
        assert FieldType.NUMBER == FieldType.NUMBER

    def test_field_type_string_representation(self):
        """Test string representation of FieldType."""
        assert str(FieldType.TEXT) == "text"
        assert str(FieldType.BOOLEAN) == "boolean"
        assert str(FieldType.NUMBER) == "number"

    def test_field_type_membership(self):
        """Test membership in FieldType enum."""
        all_types = list(FieldType)
        assert FieldType.TEXT in all_types
        assert FieldType.BOOLEAN in all_types
        assert FieldType.DATE in all_types
        assert FieldType.NUMBER in all_types
        assert FieldType.CHECKBOX in all_types
        assert FieldType.RADIO in all_types
        assert FieldType.DROPDOWN in all_types
        assert len(all_types) == 7


class TestFieldCategory:
    """Test the FieldCategory enum value object."""

    def test_field_category_values(self):
        """Test that FieldCategory enum has all required values."""
        assert FieldCategory.PERSONAL.value == "personal"
        assert FieldCategory.ADDRESS.value == "address"
        assert FieldCategory.CONTACT.value == "contact"
        assert FieldCategory.FINANCIAL.value == "financial"
        assert FieldCategory.EMPLOYMENT.value == "employment"
        assert FieldCategory.OTHER.value == "other"

    def test_field_category_immutable(self):
        """Test that FieldCategory enum values are immutable."""
        category = FieldCategory.PERSONAL
        with pytest.raises(AttributeError):
            category.value = "modified"  # type: ignore

    def test_field_category_equality(self):
        """Test equality comparison between FieldCategory values."""
        assert FieldCategory.PERSONAL == FieldCategory.PERSONAL
        assert FieldCategory.PERSONAL != FieldCategory.ADDRESS  # type: ignore[comparison-overlap]
        assert FieldCategory.FINANCIAL == FieldCategory.FINANCIAL

    def test_field_category_string_representation(self):
        """Test string representation of FieldCategory."""
        assert str(FieldCategory.PERSONAL) == "personal"
        assert str(FieldCategory.ADDRESS) == "address"
        assert str(FieldCategory.FINANCIAL) == "financial"

    def test_field_category_membership(self):
        """Test membership in FieldCategory enum."""
        all_categories = list(FieldCategory)
        assert FieldCategory.PERSONAL in all_categories
        assert FieldCategory.ADDRESS in all_categories
        assert FieldCategory.CONTACT in all_categories
        assert FieldCategory.FINANCIAL in all_categories
        assert FieldCategory.EMPLOYMENT in all_categories
        assert FieldCategory.OTHER in all_categories
        assert len(all_categories) == 6


class TestFilePath:
    """Test the FilePath value object."""

    def test_file_path_creation_valid(self):
        """Test creating a valid FilePath."""
        file_path = FilePath("/path/to/file.pdf")
        assert file_path.path == "/path/to/file.pdf"
        assert str(file_path) == "/path/to/file.pdf"

    def test_file_path_immutable(self):
        """Test that FilePath is immutable."""
        file_path = FilePath("/path/to/file.pdf")
        with pytest.raises(AttributeError):
            file_path.path = "/new/path"  # type: ignore

    def test_file_path_empty_raises_error(self):
        """Test that empty path raises ValidationError."""
        with pytest.raises(ValidationError, match="File path cannot be empty"):
            FilePath("")

    def test_file_path_non_string_raises_error(self):
        """Test that non-string path raises ValidationError."""
        with pytest.raises(ValidationError, match="File path must be a string"):
            FilePath(123)  # type: ignore

    def test_file_path_null_bytes_raises_error(self):
        """Test that path with null bytes raises ValidationError."""
        with pytest.raises(ValidationError, match="cannot contain null bytes"):
            FilePath("/path/to\x00/file.pdf")

    def test_file_path_as_path(self):
        """Test conversion to pathlib.Path."""
        file_path = FilePath("/path/to/file.pdf")
        path_obj = file_path.as_path()
        assert str(path_obj) == "/path/to/file.pdf"
        from pathlib import Path

        assert isinstance(path_obj, Path)

    def test_file_path_is_pdf(self):
        """Test PDF detection."""
        assert FilePath("/path/to/file.pdf").is_pdf() is True
        assert FilePath("/path/to/FILE.PDF").is_pdf() is True
        assert FilePath("/path/to/file.txt").is_pdf() is False
        assert FilePath("/path/to/file").is_pdf() is False

    def test_file_path_exists(self, tmp_path):
        """Test file existence check."""
        # Create a temporary file
        test_file = tmp_path / "test.pdf"
        test_file.touch()

        existing_path = FilePath(str(test_file))
        assert existing_path.exists() is True

        non_existing_path = FilePath(str(tmp_path / "nonexistent.pdf"))
        assert non_existing_path.exists() is False

    def test_file_path_equality(self):
        """Test equality comparison."""
        path1 = FilePath("/path/to/file.pdf")
        path2 = FilePath("/path/to/file.pdf")
        path3 = FilePath("/path/to/other.pdf")

        assert path1 == path2
        assert path1 != path3
        assert hash(path1) == hash(path2)

    def test_file_path_as_dict_key(self):
        """Test that FilePath can be used as dictionary key."""
        path1 = FilePath("/path/to/file.pdf")
        path2 = FilePath("/path/to/file.pdf")

        data = {path1: "value1"}
        data[path2] = "value2"

        # Should have only one entry since paths are equal
        assert len(data) == 1
        assert data[path1] == "value2"


class TestFieldValue:
    """Test the FieldValue value object."""

    def test_field_value_creation(self):
        """Test creating a FieldValue."""
        field_value = FieldValue("test", FieldType.TEXT)
        assert field_value.value == "test"
        assert field_value.field_type == FieldType.TEXT

    def test_field_value_immutable(self):
        """Test that FieldValue is immutable."""
        field_value = FieldValue("test", FieldType.TEXT)
        with pytest.raises(AttributeError):
            field_value.value = "modified"  # type: ignore

    def test_field_value_invalid_field_type_raises_error(self):
        """Test that invalid field_type raises ValidationError."""
        with pytest.raises(ValidationError, match="field_type must be a FieldType enum"):
            FieldValue("test", "not_an_enum")  # type: ignore

    def test_field_value_as_str(self):
        """Test conversion to string."""
        assert FieldValue("test", FieldType.TEXT).as_str() == "test"
        assert FieldValue(123, FieldType.NUMBER).as_str() == "123"
        assert FieldValue(True, FieldType.BOOLEAN).as_str() == "True"
        assert FieldValue(None, FieldType.TEXT).as_str() == ""

    def test_field_value_as_bool_valid(self):
        """Test valid boolean conversions."""
        # Direct boolean
        assert FieldValue(True, FieldType.BOOLEAN).as_bool() is True
        assert FieldValue(False, FieldType.BOOLEAN).as_bool() is False

        # String representations
        assert FieldValue("true", FieldType.BOOLEAN).as_bool() is True
        assert FieldValue("True", FieldType.BOOLEAN).as_bool() is True
        assert FieldValue("yes", FieldType.BOOLEAN).as_bool() is True
        assert FieldValue("1", FieldType.BOOLEAN).as_bool() is True
        assert FieldValue("on", FieldType.BOOLEAN).as_bool() is True

        assert FieldValue("false", FieldType.BOOLEAN).as_bool() is False
        assert FieldValue("False", FieldType.BOOLEAN).as_bool() is False
        assert FieldValue("no", FieldType.BOOLEAN).as_bool() is False
        assert FieldValue("0", FieldType.BOOLEAN).as_bool() is False
        assert FieldValue("off", FieldType.BOOLEAN).as_bool() is False
        assert FieldValue("", FieldType.BOOLEAN).as_bool() is False

        # Numeric values
        assert FieldValue(1, FieldType.BOOLEAN).as_bool() is True
        assert FieldValue(0, FieldType.BOOLEAN).as_bool() is False
        assert FieldValue(1.5, FieldType.BOOLEAN).as_bool() is True
        assert FieldValue(0.0, FieldType.BOOLEAN).as_bool() is False

        # Checkbox type also supports boolean conversion
        assert FieldValue(True, FieldType.CHECKBOX).as_bool() is True
        assert FieldValue(False, FieldType.CHECKBOX).as_bool() is False

    def test_field_value_as_bool_invalid_field_type(self):
        """Test that non-boolean field types raise error."""
        with pytest.raises(ValidationError, match="Cannot convert .* field to boolean"):
            FieldValue("text", FieldType.TEXT).as_bool()

        with pytest.raises(ValidationError, match="Cannot convert .* field to boolean"):
            FieldValue(123, FieldType.NUMBER).as_bool()

    def test_field_value_as_bool_invalid_string(self):
        """Test that invalid boolean string raises error."""
        with pytest.raises(ValidationError, match="Cannot convert string .* to boolean"):
            FieldValue("maybe", FieldType.BOOLEAN).as_bool()

    def test_field_value_as_bool_invalid_type(self):
        """Test that invalid type raises error."""
        with pytest.raises(ValidationError, match="Cannot convert .* to boolean"):
            FieldValue(["list"], FieldType.BOOLEAN).as_bool()

    def test_field_value_as_int_valid(self):
        """Test valid integer conversions."""
        assert FieldValue(123, FieldType.NUMBER).as_int() == 123
        assert FieldValue(123.7, FieldType.NUMBER).as_int() == 123
        assert FieldValue("456", FieldType.NUMBER).as_int() == 456
        assert FieldValue("123.0", FieldType.NUMBER).as_int() == 123
        assert FieldValue("1,234", FieldType.NUMBER).as_int() == 1234
        assert FieldValue(" 789 ", FieldType.NUMBER).as_int() == 789

    def test_field_value_as_int_invalid_field_type(self):
        """Test that non-number field types raise error."""
        with pytest.raises(ValidationError, match="Cannot convert .* field to integer"):
            FieldValue("text", FieldType.TEXT).as_int()

    def test_field_value_as_int_invalid_string(self):
        """Test that invalid number string raises error."""
        with pytest.raises(ValidationError, match="Cannot convert string .* to integer"):
            FieldValue("not a number", FieldType.NUMBER).as_int()

    def test_field_value_as_int_invalid_type(self):
        """Test that invalid type raises error."""
        with pytest.raises(ValidationError, match="Cannot convert .* to integer"):
            FieldValue(["list"], FieldType.NUMBER).as_int()

    def test_field_value_as_float_valid(self):
        """Test valid float conversions."""
        assert FieldValue(123, FieldType.NUMBER).as_float() == 123.0
        assert FieldValue(123.45, FieldType.NUMBER).as_float() == 123.45
        assert FieldValue("456.78", FieldType.NUMBER).as_float() == 456.78
        assert FieldValue("1,234.56", FieldType.NUMBER).as_float() == 1234.56
        assert FieldValue(" 789.01 ", FieldType.NUMBER).as_float() == 789.01

    def test_field_value_as_float_invalid_field_type(self):
        """Test that non-number field types raise error."""
        with pytest.raises(ValidationError, match="Cannot convert .* field to float"):
            FieldValue("text", FieldType.TEXT).as_float()

    def test_field_value_as_float_invalid_string(self):
        """Test that invalid float string raises error."""
        with pytest.raises(ValidationError, match="Cannot convert string .* to float"):
            FieldValue("not a number", FieldType.NUMBER).as_float()

    def test_field_value_as_float_invalid_type(self):
        """Test that invalid type raises error."""
        with pytest.raises(ValidationError, match="Cannot convert .* to float"):
            FieldValue({"dict": "value"}, FieldType.NUMBER).as_float()

    def test_field_value_is_empty(self):
        """Test empty value detection."""
        assert FieldValue(None, FieldType.TEXT).is_empty() is True
        assert FieldValue("", FieldType.TEXT).is_empty() is True
        assert FieldValue("  ", FieldType.TEXT).is_empty() is True
        assert FieldValue([], FieldType.TEXT).is_empty() is True
        assert FieldValue({}, FieldType.TEXT).is_empty() is True
        assert FieldValue((), FieldType.TEXT).is_empty() is True

        assert FieldValue("text", FieldType.TEXT).is_empty() is False
        assert FieldValue(0, FieldType.NUMBER).is_empty() is False
        assert FieldValue(False, FieldType.BOOLEAN).is_empty() is False
        assert FieldValue([1], FieldType.TEXT).is_empty() is False

    def test_field_value_str_representation(self):
        """Test string representation."""
        assert str(FieldValue("test", FieldType.TEXT)) == "test"
        assert str(FieldValue(123, FieldType.NUMBER)) == "123"
        assert str(FieldValue(None, FieldType.TEXT)) == ""

    def test_field_value_equality(self):
        """Test equality comparison."""
        value1 = FieldValue("test", FieldType.TEXT)
        value2 = FieldValue("test", FieldType.TEXT)
        value3 = FieldValue("other", FieldType.TEXT)
        value4 = FieldValue("test", FieldType.NUMBER)

        assert value1 == value2
        assert value1 != value3
        assert value1 != value4
        assert hash(value1) == hash(value2)

        # Test comparison with non-FieldValue object
        assert value1 != "test"
        assert value1 != 123
        assert value1 is not None

    def test_field_value_as_dict_key(self):
        """Test that FieldValue can be used as dictionary key."""
        value1 = FieldValue("test", FieldType.TEXT)
        value2 = FieldValue("test", FieldType.TEXT)

        data = {value1: "data1"}
        data[value2] = "data2"

        # Should have only one entry since values are equal
        assert len(data) == 1
        assert data[value1] == "data2"

    def test_field_value_with_none(self):
        """Test FieldValue with None value."""
        value = FieldValue(None, FieldType.TEXT)
        assert value.value is None
        assert value.as_str() == ""
        assert value.is_empty() is True


class TestValueObjectsIntegration:
    """Integration tests for value objects working together."""

    def test_field_value_with_all_field_types(self):
        """Test that FieldValue works with all FieldType values."""
        for field_type in FieldType:
            # Should not raise any errors
            value = FieldValue("test", field_type)
            assert value.field_type == field_type

    def test_file_path_with_field_value(self):
        """Test combining FilePath and FieldValue."""
        path = FilePath("/path/to/form.pdf")
        path_value = FieldValue(str(path), FieldType.TEXT)

        assert path_value.as_str() == "/path/to/form.pdf"
        assert not path_value.is_empty()

    def test_immutability_across_value_objects(self):
        """Test that all value objects maintain immutability."""
        # Enum immutability
        with pytest.raises(AttributeError):
            FieldType.TEXT.value = "modified"  # type: ignore

        with pytest.raises(AttributeError):
            FieldCategory.PERSONAL.value = "modified"  # type: ignore

        # Frozen dataclass immutability
        file_path = FilePath("/path/to/file.pdf")
        with pytest.raises(AttributeError):
            file_path.path = "/new/path"  # type: ignore

        field_value = FieldValue("test", FieldType.TEXT)
        with pytest.raises(AttributeError):
            field_value.value = "modified"  # type: ignore
