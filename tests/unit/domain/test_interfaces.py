"""Structural tests for domain interfaces.

These tests verify that the domain protocols are properly defined and that
concrete implementations satisfy the protocol contracts.
"""

from typing import Any

import pytest

from form_filler.domain.interfaces import (
    DataRepository,
    FieldCategorizer,
    FieldMatcher,
    LLMProvider,
    PDFProcessor,
)
from form_filler.domain.models import FieldCategory, FieldMapping, FieldType, FormField
from form_filler.infrastructure.pdf.pypdfform_adapter import PyPDFFormAdapter
from form_filler.infrastructure.persistence.json_repository import JSONRepository
from form_filler.infrastructure.persistence.yaml_repository import YAMLRepository


class TestPDFProcessorProtocol:
    """Test PDFProcessor protocol structure and runtime checking."""

    def test_protocol_is_runtime_checkable(self):
        """Verify PDFProcessor is runtime checkable."""
        # PyPDFFormAdapter should satisfy the protocol
        adapter = PyPDFFormAdapter()
        assert isinstance(adapter, PDFProcessor)

    def test_protocol_has_required_methods(self):
        """Verify PDFProcessor protocol defines all required methods."""
        required_methods = [
            "extract_schema",
            "extract_fields",
            "fill_form",
            "validate_form",
        ]

        for method_name in required_methods:
            assert hasattr(PDFProcessor, method_name), f"Missing method: {method_name}"

    def test_concrete_implementation_satisfies_protocol(self):
        """Verify PyPDFFormAdapter implements all PDFProcessor methods."""
        adapter = PyPDFFormAdapter()

        # Check all required methods exist
        assert callable(adapter.extract_schema)
        assert callable(adapter.extract_fields)
        assert callable(adapter.fill_form)
        assert callable(adapter.validate_form)


class TestDataRepositoryProtocol:
    """Test DataRepository protocol structure and runtime checking."""

    def test_protocol_is_runtime_checkable(self):
        """Verify DataRepository is runtime checkable."""
        # Both JSON and YAML repositories should satisfy the protocol
        json_repo = JSONRepository()
        yaml_repo = YAMLRepository()

        assert isinstance(json_repo, DataRepository)
        assert isinstance(yaml_repo, DataRepository)

    def test_protocol_has_required_methods(self):
        """Verify DataRepository protocol defines all required methods."""
        required_methods = ["save", "load", "exists", "list_profiles"]

        for method_name in required_methods:
            assert hasattr(DataRepository, method_name), f"Missing method: {method_name}"

    def test_json_repository_satisfies_protocol(self):
        """Verify JSONRepository implements all DataRepository methods."""
        repo = JSONRepository()

        # Check all required methods exist
        assert callable(repo.save)
        assert callable(repo.load)
        assert callable(repo.exists)
        assert callable(repo.list_profiles)

    def test_yaml_repository_satisfies_protocol(self):
        """Verify YAMLRepository implements all DataRepository methods."""
        repo = YAMLRepository()

        # Check all required methods exist
        assert callable(repo.save)
        assert callable(repo.load)
        assert callable(repo.exists)
        assert callable(repo.list_profiles)


class TestLLMProviderProtocol:
    """Test LLMProvider protocol structure."""

    def test_protocol_is_runtime_checkable(self):
        """Verify LLMProvider is runtime checkable."""

        # Create a mock implementation
        class MockLLMProvider:
            def generate_text(
                self,
                prompt: str,
                max_length: int = 512,
                temperature: float = 0.7,
                **kwargs: Any,
            ) -> str:
                return "Generated text"

            def extract_structured_data(
                self, text: str, schema: dict[str, type], **kwargs: Any
            ) -> dict[str, Any]:
                return {"extracted": "data"}

        mock = MockLLMProvider()
        assert isinstance(mock, LLMProvider)

    def test_protocol_has_required_methods(self):
        """Verify LLMProvider protocol defines all required methods."""
        required_methods = ["generate_text", "extract_structured_data"]

        for method_name in required_methods:
            assert hasattr(LLMProvider, method_name), f"Missing method: {method_name}"

    def test_mock_implementation_satisfies_protocol(self):
        """Verify a mock LLM implementation satisfies the protocol."""

        class MockLLM:
            def generate_text(
                self,
                prompt: str,
                max_length: int = 512,
                temperature: float = 0.7,
                **kwargs: Any,
            ) -> str:
                return f"Response to: {prompt}"

            def extract_structured_data(
                self, text: str, schema: dict[str, type], **kwargs: Any
            ) -> dict[str, Any]:
                return dict.fromkeys(schema.keys())

        mock = MockLLM()
        assert isinstance(mock, LLMProvider)

        # Test method calls
        result = mock.generate_text("test prompt")
        assert isinstance(result, str)

        data = mock.extract_structured_data("test", {"name": str})
        assert isinstance(data, dict)


class TestFieldMatcherProtocol:
    """Test FieldMatcher protocol structure."""

    def test_protocol_is_runtime_checkable(self):
        """Verify FieldMatcher is runtime checkable."""

        # Create a mock implementation
        class MockFieldMatcher:
            def match_fields(
                self,
                user_fields: list[str],
                form_fields: list[FormField],
                min_confidence: float = 0.7,
            ) -> list[FieldMapping]:
                return []

            def fuzzy_match(
                self, field_name: str, candidates: list[str], threshold: float = 0.6
            ) -> list[tuple[str, float]]:
                return []

            def confidence_score(
                self,
                user_field: str,
                form_field: str,
                context: dict[str, Any] | None = None,
            ) -> float:
                return 1.0 if user_field == form_field else 0.5

        mock = MockFieldMatcher()
        assert isinstance(mock, FieldMatcher)

    def test_protocol_has_required_methods(self):
        """Verify FieldMatcher protocol defines all required methods."""
        required_methods = ["match_fields", "fuzzy_match", "confidence_score"]

        for method_name in required_methods:
            assert hasattr(FieldMatcher, method_name), f"Missing method: {method_name}"

    def test_mock_implementation_satisfies_protocol(self):
        """Verify a mock field matcher satisfies the protocol."""

        class SimpleFieldMatcher:
            def match_fields(
                self,
                user_fields: list[str],
                form_fields: list[FormField],
                min_confidence: float = 0.7,
            ) -> list[FieldMapping]:
                """Simple exact matching."""
                mappings = []
                form_field_names = {f.name: f for f in form_fields}

                for user_field in user_fields:
                    if user_field in form_field_names:
                        mappings.append(
                            FieldMapping(
                                user_field=user_field,
                                form_field=user_field,
                                confidence=1.0,
                            )
                        )
                return mappings

            def fuzzy_match(
                self, field_name: str, candidates: list[str], threshold: float = 0.6
            ) -> list[tuple[str, float]]:
                """Simple substring matching."""
                matches = []
                for candidate in candidates:
                    if field_name.lower() in candidate.lower():
                        # Simple similarity score based on substring match
                        score = min(len(field_name) / len(candidate), 1.0)
                        matches.append((candidate, score))
                    elif candidate.lower() in field_name.lower():
                        score = min(len(candidate) / len(field_name), 1.0)
                        matches.append((candidate, score))
                # Filter by threshold and sort
                matches = [(c, s) for c, s in matches if s >= threshold]
                return sorted(matches, key=lambda x: x[1], reverse=True)

            def confidence_score(
                self,
                user_field: str,
                form_field: str,
                context: dict[str, Any] | None = None,
            ) -> float:
                """Calculate confidence based on exact or fuzzy match."""
                if user_field == form_field:
                    return 1.0
                elif user_field.lower() in form_field.lower():
                    return 0.8
                else:
                    return 0.0

        matcher = SimpleFieldMatcher()
        assert isinstance(matcher, FieldMatcher)

        # Test exact match
        user_fields = ["email", "name"]
        form_fields = [
            FormField(name="email", field_type=FieldType.TEXT, default_value="", required=True),
            FormField(name="name", field_type=FieldType.TEXT, default_value="", required=True),
        ]
        mappings = matcher.match_fields(user_fields, form_fields)
        assert len(mappings) == 2
        assert all(m.confidence == 1.0 for m in mappings)

        # Test fuzzy match with lower threshold
        matches = matcher.fuzzy_match("email", ["email_address", "e_mail", "phone"], threshold=0.3)
        assert len(matches) > 0
        assert matches[0][0] in ["email_address", "e_mail"]  # Should match email-related fields

        # Test confidence score
        score = matcher.confidence_score("email", "email")
        assert score == 1.0


class TestFieldCategorizerABC:
    """Test FieldCategorizer abstract base class."""

    def test_abc_cannot_be_instantiated(self):
        """Verify FieldCategorizer cannot be instantiated directly."""
        with pytest.raises(TypeError):
            FieldCategorizer()  # type: ignore[abstract]

    def test_abc_requires_categorize_method(self):
        """Verify FieldCategorizer requires categorize method implementation."""

        # Class without categorize should fail
        with pytest.raises(TypeError):

            class IncompleteCategorizer(FieldCategorizer):
                pass

            IncompleteCategorizer()  # type: ignore[abstract]

    def test_concrete_implementation_works(self):
        """Verify a concrete implementation of FieldCategorizer works."""

        class SimpleCategorizer(FieldCategorizer):
            def categorize(self, field: FormField) -> FieldCategory:
                """Simple rule-based categorization."""
                name_lower = field.name.lower()

                if any(word in name_lower for word in ["name", "first", "last"]):
                    return FieldCategory.PERSONAL
                elif any(word in name_lower for word in ["street", "city", "zip"]):
                    return FieldCategory.ADDRESS
                elif any(word in name_lower for word in ["email", "phone"]):
                    return FieldCategory.CONTACT
                else:
                    return FieldCategory.OTHER

        categorizer = SimpleCategorizer()

        # Test categorization
        field = FormField(
            name="first_name", field_type=FieldType.TEXT, default_value="", required=True
        )
        category = categorizer.categorize(field)
        assert category == FieldCategory.PERSONAL


class TestProtocolDocumentation:
    """Test that protocols have proper documentation."""

    def test_protocols_have_docstrings(self):
        """Verify all protocols have docstrings."""
        protocols = [
            PDFProcessor,
            DataRepository,
            LLMProvider,
            FieldMatcher,
            FieldCategorizer,
        ]

        for protocol in protocols:
            assert protocol.__doc__ is not None, f"{protocol.__name__} missing docstring"
            assert len(protocol.__doc__) > 50, f"{protocol.__name__} docstring too short"

    def test_protocol_methods_have_docstrings(self):
        """Verify protocol methods have docstrings."""
        # Test PDFProcessor methods
        assert PDFProcessor.extract_schema.__doc__ is not None
        assert PDFProcessor.extract_fields.__doc__ is not None
        assert PDFProcessor.fill_form.__doc__ is not None
        assert PDFProcessor.validate_form.__doc__ is not None

        # Test DataRepository methods
        assert DataRepository.save.__doc__ is not None
        assert DataRepository.load.__doc__ is not None
        assert DataRepository.exists.__doc__ is not None
        assert DataRepository.list_profiles.__doc__ is not None

        # Test LLMProvider methods
        assert LLMProvider.generate_text.__doc__ is not None
        assert LLMProvider.extract_structured_data.__doc__ is not None

        # Test FieldMatcher methods
        assert FieldMatcher.match_fields.__doc__ is not None
        assert FieldMatcher.fuzzy_match.__doc__ is not None
        assert FieldMatcher.confidence_score.__doc__ is not None

        # Test FieldCategorizer methods
        assert FieldCategorizer.categorize.__doc__ is not None
