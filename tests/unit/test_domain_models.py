"""Unit tests for domain models."""

import pytest

from form_filler.domain.models import FieldCategory, FieldType, FormField, PDFForm


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
