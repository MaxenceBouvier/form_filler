"""Unit tests for domain models."""

from dataclasses import FrozenInstanceError

import pytest

from form_filler.domain.exceptions import ValidationError
from form_filler.domain.models import (
    FieldCategory,
    FieldMapping,
    FieldType,
    FormField,
    PDFForm,
    UserData,
)


class TestFormField:
    """Test the FormField domain model."""

    def test_form_field_creation(self):
        """Test creating a FormField."""
        field = FormField(
            name="test_field",
            field_type=FieldType.TEXT,
            default_value="",
            required=True,
            category=FieldCategory.PERSONAL,
        )

        assert field.name == "test_field"
        assert field.field_type == FieldType.TEXT
        assert field.default_value == ""
        assert field.required is True
        assert field.category == FieldCategory.PERSONAL

    def test_form_field_to_dict(self):
        """Test converting FormField to dictionary."""
        field = FormField(
            name="test_field",
            field_type=FieldType.BOOLEAN,
            default_value=False,
            required=False,
            category=FieldCategory.FINANCIAL,
            options=["Yes", "No"],
        )

        result = field.to_dict()

        assert result["name"] == "test_field"
        assert result["type"] == "boolean"
        assert result["default_value"] is False
        assert result["required"] is False
        assert result["category"] == "financial"
        assert result["options"] == ["Yes", "No"]


class TestPDFForm:
    """Test the PDFForm domain model."""

    @pytest.fixture
    def sample_fields(self):
        """Create sample fields for testing."""
        return [
            FormField(
                name="name",
                field_type=FieldType.TEXT,
                default_value="",
                category=FieldCategory.PERSONAL,
            ),
            FormField(
                name="address",
                field_type=FieldType.TEXT,
                default_value="",
                category=FieldCategory.ADDRESS,
            ),
            FormField(
                name="income",
                field_type=FieldType.NUMBER,
                default_value=0,
                category=FieldCategory.FINANCIAL,
            ),
        ]

    def test_pdf_form_creation(self, sample_fields):
        """Test creating a PDFForm."""
        pdf_form = PDFForm(path="/path/to/form.pdf", fields=sample_fields, metadata={})

        assert pdf_form.path == "/path/to/form.pdf"
        assert len(pdf_form.fields) == 3
        assert pdf_form.field_count == 3

    def test_get_fields_by_category(self, sample_fields):
        """Test getting fields by category."""
        pdf_form = PDFForm(path="/path/to/form.pdf", fields=sample_fields, metadata={})

        personal_fields = pdf_form.get_fields_by_category(FieldCategory.PERSONAL)
        assert len(personal_fields) == 1
        assert personal_fields[0].name == "name"

        financial_fields = pdf_form.get_fields_by_category(FieldCategory.FINANCIAL)
        assert len(financial_fields) == 1
        assert financial_fields[0].name == "income"

    def test_to_stub_dict(self, sample_fields):
        """Test generating stub dictionary."""
        pdf_form = PDFForm(path="/path/to/form.pdf", fields=sample_fields, metadata={})

        stub = pdf_form.to_stub_dict()

        assert stub["name"] == ""
        assert stub["address"] == ""
        assert stub["income"] == 0
        assert len(stub) == 3

    def test_pdf_form_frozen(self, sample_fields):
        """Test that PDFForm is immutable (frozen)."""
        pdf_form = PDFForm(path="/path/to/form.pdf", fields=sample_fields, metadata={})

        with pytest.raises(FrozenInstanceError):
            pdf_form.path = "/new/path.pdf"  # type: ignore[misc]

    def test_pdf_form_fields_as_tuple(self, sample_fields):
        """Test that fields are converted to tuple for immutability."""
        pdf_form = PDFForm(path="/path/to/form.pdf", fields=sample_fields, metadata={})

        assert isinstance(pdf_form.fields, tuple)
        assert len(pdf_form.fields) == 3


class TestFormFieldImmutability:
    """Test FormField immutability and special methods."""

    def test_form_field_frozen(self):
        """Test that FormField is immutable (frozen)."""
        field = FormField(name="test_field", field_type=FieldType.TEXT, default_value="")

        with pytest.raises(FrozenInstanceError):
            field.name = "new_name"  # type: ignore[misc]

    def test_form_field_equality(self):
        """Test FormField equality comparison."""
        field1 = FormField(
            name="test_field",
            field_type=FieldType.TEXT,
            default_value="",
            required=True,
        )
        field2 = FormField(
            name="test_field",
            field_type=FieldType.TEXT,
            default_value="",
            required=True,
        )
        field3 = FormField(
            name="different_field",
            field_type=FieldType.TEXT,
            default_value="",
            required=True,
        )

        assert field1 == field2
        assert field1 != field3

    def test_form_field_repr(self):
        """Test FormField string representation."""
        field = FormField(
            name="test_field",
            field_type=FieldType.TEXT,
            default_value="",
            category=FieldCategory.PERSONAL,
        )

        repr_str = repr(field)
        assert "FormField" in repr_str
        assert "test_field" in repr_str
        assert "FieldType.TEXT" in repr_str


class TestUserData:
    """Test the UserData domain model."""

    def test_user_data_creation(self):
        """Test creating UserData."""
        user_data = UserData(
            data={"first_name": "John", "last_name": "Doe", "age": 30},
            metadata={"source": "manual_entry"},
        )

        assert user_data.data["first_name"] == "John"
        assert user_data.data["age"] == 30
        assert user_data.metadata["source"] == "manual_entry"

    def test_user_data_get(self):
        """Test getting values from UserData."""
        user_data = UserData(data={"name": "Alice", "email": "alice@example.com"})

        assert user_data.get("name") == "Alice"
        assert user_data.get("email") == "alice@example.com"
        assert user_data.get("missing_field") is None
        assert user_data.get("missing_field", "default") == "default"

    def test_user_data_has_field(self):
        """Test checking field existence."""
        user_data = UserData(data={"name": "Bob", "age": 25})

        assert user_data.has_field("name") is True
        assert user_data.has_field("age") is True
        assert user_data.has_field("missing") is False

    def test_user_data_to_dict(self):
        """Test converting UserData to dictionary."""
        user_data = UserData(data={"name": "Charlie"}, metadata={"version": "1.0"})

        result = user_data.to_dict()

        assert result["data"]["name"] == "Charlie"
        assert result["metadata"]["version"] == "1.0"

    def test_user_data_from_dict(self):
        """Test creating UserData from dictionary."""
        source = {
            "data": {"name": "David", "age": 40},
            "metadata": {"source": "import"},
        }

        user_data = UserData.from_dict(source)

        assert user_data.get("name") == "David"
        assert user_data.get("age") == 40
        assert user_data.metadata["source"] == "import"

    def test_user_data_from_dict_without_metadata(self):
        """Test creating UserData from dict without metadata."""
        source = {"data": {"name": "Eve"}}

        user_data = UserData.from_dict(source)

        assert user_data.get("name") == "Eve"
        assert user_data.metadata == {}

    def test_user_data_validation_invalid_data_type(self):
        """Test validation fails for non-dict data."""
        with pytest.raises(ValidationError, match="data must be a dictionary"):
            UserData(data="not a dict")  # type: ignore

    def test_user_data_validation_invalid_metadata_type(self):
        """Test validation fails for non-dict metadata."""
        with pytest.raises(ValidationError, match="metadata must be a dictionary"):
            UserData(data={}, metadata="not a dict")  # type: ignore

    def test_user_data_from_dict_validation_no_data_key(self):
        """Test from_dict validation for missing data key."""
        with pytest.raises(ValidationError, match="must contain 'data' key"):
            UserData.from_dict({"metadata": {}})

    def test_user_data_from_dict_validation_invalid_source(self):
        """Test from_dict validation for invalid source type."""
        with pytest.raises(ValidationError, match="Source must be a dictionary"):
            UserData.from_dict("not a dict")  # type: ignore

    def test_user_data_frozen(self):
        """Test that UserData is immutable (frozen)."""
        user_data = UserData(data={"name": "Frank"})

        with pytest.raises(FrozenInstanceError):
            user_data.data = {"name": "George"}  # type: ignore[misc]

    def test_user_data_default_metadata(self):
        """Test UserData with default metadata."""
        user_data = UserData(data={"name": "Helen"})

        assert user_data.metadata == {}
        assert user_data.get("name") == "Helen"


class TestFieldMapping:
    """Test the FieldMapping domain model."""

    def test_field_mapping_creation(self):
        """Test creating FieldMapping."""
        mapping = FieldMapping(
            user_field="first_name",
            form_field="firstName",
            transform="capitalize",
            confidence=0.95,
        )

        assert mapping.user_field == "first_name"
        assert mapping.form_field == "firstName"
        assert mapping.transform == "capitalize"
        assert mapping.confidence == 0.95

    def test_field_mapping_is_exact_match_true(self):
        """Test exact match detection when fields are identical."""
        mapping = FieldMapping(user_field="email", form_field="email")

        assert mapping.is_exact_match() is True

    def test_field_mapping_is_exact_match_false(self):
        """Test exact match detection when fields differ."""
        mapping = FieldMapping(user_field="phone", form_field="phone_number")

        assert mapping.is_exact_match() is False

    def test_field_mapping_to_dict(self):
        """Test converting FieldMapping to dictionary."""
        mapping = FieldMapping(
            user_field="address",
            form_field="street_address",
            transform="format_address",
            confidence=0.8,
        )

        result = mapping.to_dict()

        assert result["user_field"] == "address"
        assert result["form_field"] == "street_address"
        assert result["transform"] == "format_address"
        assert result["confidence"] == 0.8

    def test_field_mapping_default_values(self):
        """Test FieldMapping with default values."""
        mapping = FieldMapping(user_field="name", form_field="full_name")

        assert mapping.transform is None
        assert mapping.confidence == 1.0

    def test_field_mapping_validation_empty_user_field(self):
        """Test validation fails for empty user_field."""
        with pytest.raises(ValidationError, match="user_field must be a non-empty string"):
            FieldMapping(user_field="", form_field="test")

    def test_field_mapping_validation_empty_form_field(self):
        """Test validation fails for empty form_field."""
        with pytest.raises(ValidationError, match="form_field must be a non-empty string"):
            FieldMapping(user_field="test", form_field="")

    def test_field_mapping_validation_invalid_confidence_too_high(self):
        """Test validation fails for confidence > 1.0."""
        with pytest.raises(ValidationError, match="confidence must be between 0.0 and 1.0"):
            FieldMapping(user_field="test", form_field="test", confidence=1.5)

    def test_field_mapping_validation_invalid_confidence_too_low(self):
        """Test validation fails for confidence < 0.0."""
        with pytest.raises(ValidationError, match="confidence must be between 0.0 and 1.0"):
            FieldMapping(user_field="test", form_field="test", confidence=-0.1)

    def test_field_mapping_frozen(self):
        """Test that FieldMapping is immutable (frozen)."""
        mapping = FieldMapping(user_field="name", form_field="full_name")

        with pytest.raises(FrozenInstanceError):
            mapping.user_field = "new_name"  # type: ignore[misc]

    def test_field_mapping_equality(self):
        """Test FieldMapping equality comparison."""
        mapping1 = FieldMapping(user_field="email", form_field="email_address", confidence=0.9)
        mapping2 = FieldMapping(user_field="email", form_field="email_address", confidence=0.9)
        mapping3 = FieldMapping(user_field="phone", form_field="phone_number", confidence=0.9)

        assert mapping1 == mapping2
        assert mapping1 != mapping3
