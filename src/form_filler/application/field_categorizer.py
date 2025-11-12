"""Field categorization implementation."""

import re

from form_filler.domain.interfaces import FieldCategorizer
from form_filler.domain.models import FieldCategory, FormField


class RuleBasedFieldCategorizer(FieldCategorizer):
    """Rule-based field categorizer using keyword matching."""

    def __init__(self):
        """Initialize the categorizer with predefined rules."""
        self.rules = self._build_rules()

    def _build_rules(self) -> dict[FieldCategory, list[re.Pattern]]:
        """Build categorization rules.

        Returns:
            Dictionary mapping categories to regex patterns.
            Note: Order matters! More specific patterns should be checked first.
        """
        return {
            # Check more specific categories first to avoid false matches
            FieldCategory.EMPLOYMENT: [
                re.compile(r".*employer.*", re.IGNORECASE),
                re.compile(r".*occupation.*", re.IGNORECASE),
                re.compile(r".*job.*", re.IGNORECASE),
                re.compile(r".*work.*", re.IGNORECASE),
                re.compile(r".*profession.*", re.IGNORECASE),
            ],
            FieldCategory.FINANCIAL: [
                re.compile(r".*income.*", re.IGNORECASE),
                re.compile(r".*salary.*", re.IGNORECASE),
                re.compile(r".*bank.*", re.IGNORECASE),
                re.compile(r".*account.*", re.IGNORECASE),
                re.compile(r".*tax.*", re.IGNORECASE),
                re.compile(r".*revenue.*", re.IGNORECASE),
                re.compile(r".*wealth.*", re.IGNORECASE),
            ],
            FieldCategory.CONTACT: [
                re.compile(r".*phone.*", re.IGNORECASE),
                re.compile(r".*email.*", re.IGNORECASE),
                re.compile(r".*mobile.*", re.IGNORECASE),
                re.compile(r".*tel.*", re.IGNORECASE),
                re.compile(r".*contact.*", re.IGNORECASE),
                re.compile(r".*fax.*", re.IGNORECASE),
            ],
            FieldCategory.ADDRESS: [
                re.compile(r".*address.*", re.IGNORECASE),
                re.compile(r".*street.*", re.IGNORECASE),
                re.compile(r".*city.*", re.IGNORECASE),
                re.compile(r".*state.*", re.IGNORECASE),
                re.compile(r".*zip.*", re.IGNORECASE),
                re.compile(r".*postal.*", re.IGNORECASE),
                re.compile(r".*country.*", re.IGNORECASE),
            ],
            # PERSONAL last since it has generic patterns like "name"
            FieldCategory.PERSONAL: [
                re.compile(r".*name.*", re.IGNORECASE),
                re.compile(r".*birth.*", re.IGNORECASE),
                re.compile(r".*ssn.*", re.IGNORECASE),
                re.compile(r".*social.*security.*", re.IGNORECASE),
                re.compile(r".*age.*", re.IGNORECASE),
                re.compile(r".*gender.*", re.IGNORECASE),
                re.compile(r".*sex.*", re.IGNORECASE),
            ],
        }

    def categorize(self, field: FormField) -> FieldCategory:
        """Categorize a field based on its name.

        Args:
            field: The form field to categorize.

        Returns:
            The appropriate category for the field.
        """
        for category, patterns in self.rules.items():
            for pattern in patterns:
                if pattern.match(field.name):
                    return category
        return FieldCategory.OTHER
