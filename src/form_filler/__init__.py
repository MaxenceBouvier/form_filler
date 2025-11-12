"""Form Filler - A Python utility for semi-automatically filling PDF forms."""

__version__ = "0.1.0"
__author__ = "mbouvier"

from form_filler.application import ExtractFieldsUseCase, RuleBasedFieldCategorizer
from form_filler.container import container, setup_container
from form_filler.domain import FieldCategory, FieldType, FormField, PDFForm

__all__ = [
    "FieldType",
    "FieldCategory",
    "FormField",
    "PDFForm",
    "ExtractFieldsUseCase",
    "RuleBasedFieldCategorizer",
    "container",
    "setup_container",
]
