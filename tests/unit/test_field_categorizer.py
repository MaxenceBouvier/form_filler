"""Unit tests for the field categorizer."""

import pytest

from form_filler.application.field_categorizer import RuleBasedFieldCategorizer
from form_filler.domain.models import FieldCategory, FieldType, FormField


class TestRuleBasedFieldCategorizer:
    """Test the RuleBasedFieldCategorizer."""

    @pytest.fixture
    def categorizer(self):
        """Create a field categorizer instance."""
        return RuleBasedFieldCategorizer()

    def test_categorize_personal_field(self, categorizer):
        """Test categorizing a personal field."""
        field = FormField(name="full_name", field_type=FieldType.TEXT, default_value="")
        category = categorizer.categorize(field)
        assert category == FieldCategory.PERSONAL

    def test_categorize_address_field(self, categorizer):
        """Test categorizing an address field."""
        field = FormField(name="home_address", field_type=FieldType.TEXT, default_value="")
        category = categorizer.categorize(field)
        assert category == FieldCategory.ADDRESS

    def test_categorize_financial_field(self, categorizer):
        """Test categorizing a financial field."""
        field = FormField(name="annual_income", field_type=FieldType.NUMBER, default_value=0)
        category = categorizer.categorize(field)
        assert category == FieldCategory.FINANCIAL

    def test_categorize_employment_field(self, categorizer):
        """Test categorizing an employment field."""
        field = FormField(name="employer_name", field_type=FieldType.TEXT, default_value="")
        category = categorizer.categorize(field)
        assert category == FieldCategory.EMPLOYMENT

    def test_categorize_contact_field(self, categorizer):
        """Test categorizing a contact field."""
        field = FormField(name="phone_number", field_type=FieldType.TEXT, default_value="")
        category = categorizer.categorize(field)
        assert category == FieldCategory.CONTACT

    def test_categorize_unknown_field(self, categorizer):
        """Test categorizing an unknown field."""
        field = FormField(name="random_field_xyz", field_type=FieldType.TEXT, default_value="")
        category = categorizer.categorize(field)
        assert category == FieldCategory.OTHER

    def test_case_insensitive_matching(self, categorizer):
        """Test that categorization is case insensitive."""
        field_upper = FormField(name="FULL_NAME", field_type=FieldType.TEXT, default_value="")
        field_lower = FormField(name="full_name", field_type=FieldType.TEXT, default_value="")
        field_mixed = FormField(name="Full_Name", field_type=FieldType.TEXT, default_value="")

        assert categorizer.categorize(field_upper) == FieldCategory.PERSONAL
        assert categorizer.categorize(field_lower) == FieldCategory.PERSONAL
        assert categorizer.categorize(field_mixed) == FieldCategory.PERSONAL
