"""Domain models for the form filler application."""

from dataclasses import dataclass, field
from typing import Any

from form_filler.domain.exceptions import ValidationError
from form_filler.domain.value_objects import FieldCategory, FieldType


@dataclass
class FormField:
    """Domain model for a form field.

    Represents a single field in a PDF form with its metadata and constraints.

    Attributes:
        name: The unique identifier for the form field
        field_type: The type of data this field accepts (TEXT, BOOLEAN, etc.)
        default_value: The initial/default value for this field
        required: Whether this field must be filled
        category: Optional categorization for grouping fields
        options: For CHOICE fields, the list of valid options

    Examples:
        >>> field = FormField(
        ...     name="first_name",
        ...     field_type=FieldType.TEXT,
        ...     default_value="",
        ...     required=True,
        ...     category=FieldCategory.PERSONAL
        ... )
        >>> field.name
        'first_name'
        >>> field.required
        True
    """

    name: str
    field_type: FieldType
    default_value: Any
    required: bool = False
    category: FieldCategory | None = None
    options: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Returns:
            Dictionary with field metadata, suitable for serialization.

        Examples:
            >>> field = FormField(
            ...     name="active",
            ...     field_type=FieldType.BOOLEAN,
            ...     default_value=False
            ... )
            >>> field.to_dict()
            {'name': 'active', 'type': 'boolean', 'default_value': False, 'required': False, 'category': None, 'options': None}
        """
        return {
            "name": self.name,
            "type": self.field_type.value,
            "default_value": self.default_value,
            "required": self.required,
            "category": self.category.value if self.category else None,
            "options": self.options,
        }


@dataclass
class PDFForm:
    """Domain model for a PDF form.

    Represents a complete PDF form with all its fields and metadata.

    Attributes:
        path: File system path to the PDF form
        fields: Collection of form fields in this PDF
        metadata: Additional metadata about the form (title, author, etc.)

    Examples:
        >>> fields = [
        ...     FormField(name="name", field_type=FieldType.TEXT, default_value=""),
        ...     FormField(name="active", field_type=FieldType.BOOLEAN, default_value=False),
        ... ]
        >>> form = PDFForm(path="/path/to/form.pdf", fields=fields, metadata={"title": "Tax Form"})
        >>> form.field_count
        2
        >>> stub = form.to_stub_dict()
        >>> stub["name"]
        ''
    """

    path: str
    fields: list[FormField]
    metadata: dict[str, Any]

    @property
    def field_count(self) -> int:
        """Return the number of fields in the form.

        Returns:
            Count of fields in this form.

        Examples:
            >>> fields = [FormField(name="f1", field_type=FieldType.TEXT, default_value="")]
            >>> form = PDFForm(path="/test.pdf", fields=fields, metadata={})
            >>> form.field_count
            1
        """
        return len(self.fields)

    def get_fields_by_category(self, category: FieldCategory) -> list[FormField]:
        """Get all fields of a specific category.

        Args:
            category: The category to filter by.

        Returns:
            List of fields matching the specified category.

        Examples:
            >>> personal = FormField(
            ...     name="name",
            ...     field_type=FieldType.TEXT,
            ...     default_value="",
            ...     category=FieldCategory.PERSONAL
            ... )
            >>> address = FormField(
            ...     name="address",
            ...     field_type=FieldType.TEXT,
            ...     default_value="",
            ...     category=FieldCategory.ADDRESS
            ... )
            >>> form = PDFForm(path="/test.pdf", fields=[personal, address], metadata={})
            >>> personal_fields = form.get_fields_by_category(FieldCategory.PERSONAL)
            >>> len(personal_fields)
            1
            >>> personal_fields[0].name
            'name'
        """
        return [f for f in self.fields if f.category == category]

    def to_stub_dict(self) -> dict[str, Any]:
        """Generate a stub dictionary with field names and default values.

        Returns:
            Dictionary mapping field names to their default values.

        Examples:
            >>> fields = [
            ...     FormField(name="name", field_type=FieldType.TEXT, default_value=""),
            ...     FormField(name="age", field_type=FieldType.NUMBER, default_value=0),
            ... ]
            >>> form = PDFForm(path="/test.pdf", fields=fields, metadata={})
            >>> stub = form.to_stub_dict()
            >>> stub["name"]
            ''
            >>> stub["age"]
            0
        """
        return {field.name: field.default_value for field in self.fields}


@dataclass
class UserData:
    """Domain model for user information.

    Container for user data that can be used to fill form fields.
    Provides validation and type-safe access to user information.

    Attributes:
        data: Dictionary mapping field names to their values
        metadata: Optional metadata about the user data (source, last_updated, etc.)

    Examples:
        >>> user_data = UserData(
        ...     data={"first_name": "John", "last_name": "Doe", "age": 30},
        ...     metadata={"source": "manual_entry", "last_updated": "2025-01-15"}
        ... )
        >>> user_data.get("first_name")
        'John'
        >>> user_data.get("missing_field", "default_value")
        'default_value'
        >>> user_data.has_field("age")
        True
    """

    data: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate user data on initialization."""
        if not isinstance(self.data, dict):
            raise ValidationError("UserData.data must be a dictionary")
        if not isinstance(self.metadata, dict):
            raise ValidationError("UserData.metadata must be a dictionary")

    def get(self, field_name: str, default: Any = None) -> Any:
        """Get value for a field name.

        Args:
            field_name: Name of the field to retrieve
            default: Default value if field not found

        Returns:
            The value associated with the field name, or default if not found.

        Examples:
            >>> user_data = UserData(data={"name": "Alice"})
            >>> user_data.get("name")
            'Alice'
            >>> user_data.get("missing", "N/A")
            'N/A'
        """
        return self.data.get(field_name, default)

    def has_field(self, field_name: str) -> bool:
        """Check if a field exists in the user data.

        Args:
            field_name: Name of the field to check

        Returns:
            True if the field exists, False otherwise.

        Examples:
            >>> user_data = UserData(data={"email": "test@example.com"})
            >>> user_data.has_field("email")
            True
            >>> user_data.has_field("phone")
            False
        """
        return field_name in self.data

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Returns:
            Dictionary containing data and metadata.

        Examples:
            >>> user_data = UserData(data={"name": "Bob"}, metadata={"version": "1.0"})
            >>> result = user_data.to_dict()
            >>> result["data"]["name"]
            'Bob'
            >>> result["metadata"]["version"]
            '1.0'
        """
        return {"data": self.data, "metadata": self.metadata}

    @classmethod
    def from_dict(cls, source: dict[str, Any]) -> "UserData":
        """Create UserData from a dictionary.

        Args:
            source: Dictionary with 'data' and optional 'metadata' keys

        Returns:
            New UserData instance.

        Raises:
            ValidationError: If source is invalid.

        Examples:
            >>> source = {"data": {"name": "Charlie"}, "metadata": {"version": "2.0"}}
            >>> user_data = UserData.from_dict(source)
            >>> user_data.get("name")
            'Charlie'
        """
        if not isinstance(source, dict):
            raise ValidationError("Source must be a dictionary")
        if "data" not in source:
            raise ValidationError("Source must contain 'data' key")

        return cls(data=source["data"], metadata=source.get("metadata", {}))


@dataclass
class FieldMapping:
    """Domain model for mapping user data fields to form fields.

    Represents a mapping between a user data field and a PDF form field,
    potentially with transformation logic.

    Attributes:
        user_field: Name of the field in user data
        form_field: Name of the field in the PDF form
        transform: Optional transformation function name/identifier
        confidence: Optional confidence score for fuzzy matching (0.0 to 1.0)

    Examples:
        >>> mapping = FieldMapping(
        ...     user_field="first_name",
        ...     form_field="firstName",
        ...     confidence=1.0
        ... )
        >>> mapping.user_field
        'first_name'
        >>> mapping.is_exact_match()
        False
        >>> exact = FieldMapping(user_field="name", form_field="name")
        >>> exact.is_exact_match()
        True
    """

    user_field: str
    form_field: str
    transform: str | None = None
    confidence: float = 1.0

    def __post_init__(self) -> None:
        """Validate field mapping on initialization."""
        if not self.user_field or not isinstance(self.user_field, str):
            raise ValidationError("user_field must be a non-empty string")
        if not self.form_field or not isinstance(self.form_field, str):
            raise ValidationError("form_field must be a non-empty string")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValidationError("confidence must be between 0.0 and 1.0")

    def is_exact_match(self) -> bool:
        """Check if this is an exact field name match.

        Returns:
            True if user_field and form_field are identical.

        Examples:
            >>> exact = FieldMapping(user_field="email", form_field="email")
            >>> exact.is_exact_match()
            True
            >>> fuzzy = FieldMapping(user_field="email", form_field="email_address")
            >>> fuzzy.is_exact_match()
            False
        """
        return self.user_field == self.form_field

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Returns:
            Dictionary with mapping details.

        Examples:
            >>> mapping = FieldMapping(
            ...     user_field="phone",
            ...     form_field="phone_number",
            ...     transform="format_phone",
            ...     confidence=0.9
            ... )
            >>> result = mapping.to_dict()
            >>> result["user_field"]
            'phone'
            >>> result["confidence"]
            0.9
        """
        return {
            "user_field": self.user_field,
            "form_field": self.form_field,
            "transform": self.transform,
            "confidence": self.confidence,
        }
