"""Domain validators for business rule enforcement.

This module provides pure validator functions that enforce business rules
and data constraints. All validators:
- Are pure functions (no side effects)
- Raise appropriate domain exceptions on validation failure
- Return validated data on success
"""

from typing import Any

from form_filler.domain.exceptions import DataValidationError, FieldMappingError, ValidationError
from form_filler.domain.value_objects import FieldType


def validate_field_value(
    value: Any,
    field_type: FieldType,
    field_name: str,
    required: bool = False,
    options: list[str] | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
) -> Any:
    """Validate a field value against its type and constraints.

    This is a pure function that validates a single field value according
    to its declared type and optional constraints.

    Args:
        value: The value to validate
        field_type: The expected field type
        field_name: Name of the field (for error messages)
        required: Whether the field is required (cannot be None/empty)
        options: For CHOICE/DROPDOWN fields, list of valid options
        min_value: For NUMBER fields, minimum allowed value
        max_value: For NUMBER fields, maximum allowed value

    Returns:
        The validated value (may be coerced to appropriate type)

    Raises:
        DataValidationError: If validation fails

    Examples:
        >>> validate_field_value("John", FieldType.TEXT, "first_name", required=True)
        'John'
        >>> validate_field_value(25, FieldType.NUMBER, "age", min_value=0, max_value=150)
        25
        >>> validate_field_value("Option1", FieldType.CHOICE, "color", options=["Option1", "Option2"])
        'Option1'
    """
    # Check required constraint
    if required and _is_empty(value):
        raise DataValidationError(
            f"Required field '{field_name}' cannot be empty",
            field_name=field_name,
            expected_type=field_type.value,
        )

    # If value is None or empty and not required, it's valid
    if _is_empty(value) and not required:
        return value

    # Type-specific validation
    if field_type == FieldType.TEXT:
        return _validate_text(value, field_name)

    elif field_type == FieldType.BOOLEAN or field_type == FieldType.CHECKBOX:
        return _validate_boolean(value, field_name)

    elif field_type == FieldType.NUMBER:
        return _validate_number(value, field_name, min_value, max_value)

    elif field_type == FieldType.DATE:
        return _validate_date(value, field_name)

    elif field_type in (FieldType.CHOICE, FieldType.DROPDOWN, FieldType.RADIO):
        return _validate_choice(value, field_name, options)

    elif field_type == FieldType.UNKNOWN:
        # For unknown types, just return the value as-is
        return value

    else:
        raise DataValidationError(
            f"Unknown field type: {field_type}",
            field_name=field_name,
            expected_type=field_type.value,
        )


def validate_user_data(
    user_data: dict[str, Any],
    required_fields: list[str] | None = None,
    field_types: dict[str, FieldType] | None = None,
) -> dict[str, Any]:
    """Validate complete user data structure.

    This is a pure function that validates an entire user data dictionary
    against required fields and expected types.

    Args:
        user_data: Dictionary of user data to validate
        required_fields: Optional list of field names that must be present
        field_types: Optional mapping of field names to expected types

    Returns:
        The validated user data dictionary

    Raises:
        DataValidationError: If validation fails
        ValidationError: If user_data is not a dictionary

    Examples:
        >>> data = {"name": "Alice", "age": 30}
        >>> validate_user_data(data, required_fields=["name"])
        {'name': 'Alice', 'age': 30}
        >>> validate_user_data(data, field_types={"age": FieldType.NUMBER})
        {'name': 'Alice', 'age': 30}
    """
    # Validate that user_data is a dictionary
    if not isinstance(user_data, dict):
        raise ValidationError(f"User data must be a dictionary, got {type(user_data).__name__}")

    # Check for empty data
    if not user_data:
        if required_fields:
            raise DataValidationError(
                "User data is empty but required fields are specified",
                expected_type="dict",
                actual_value=user_data,
            )
        return user_data

    # Validate required fields are present
    if required_fields:
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            raise DataValidationError(
                f"Missing required fields: {', '.join(missing_fields)}",
                expected_type="dict with required fields",
                actual_value=user_data,
            )

    # Validate field types if specified
    if field_types:
        for field_name, expected_type in field_types.items():
            if field_name in user_data:
                value = user_data[field_name]
                try:
                    validate_field_value(
                        value=value,
                        field_type=expected_type,
                        field_name=field_name,
                        required=False,  # Presence already checked above
                    )
                except DataValidationError as e:
                    # Re-raise with more context
                    raise DataValidationError(
                        f"Invalid value for field '{field_name}': {e.message}",
                        field_name=field_name,
                        expected_type=expected_type.value,
                        actual_value=value,
                    ) from e

    return user_data


def validate_field_mapping(
    user_field: str,
    form_field: str,
    confidence: float = 1.0,
    user_data: dict[str, Any] | None = None,
    form_fields: list[str] | None = None,
) -> tuple[str, str, float]:
    """Validate a field mapping between user data and form fields.

    This is a pure function that validates a mapping is well-formed and,
    optionally, that the referenced fields actually exist.

    Args:
        user_field: Name of the field in user data
        form_field: Name of the field in the form
        confidence: Confidence score for the mapping (0.0 to 1.0)
        user_data: Optional user data to verify user_field exists
        form_fields: Optional list of form field names to verify form_field exists

    Returns:
        Tuple of (user_field, form_field, confidence) if valid

    Raises:
        FieldMappingError: If mapping validation fails
        ValidationError: If parameters are invalid

    Examples:
        >>> validate_field_mapping("first_name", "firstName", confidence=0.95)
        ('first_name', 'firstName', 0.95)
        >>> validate_field_mapping("email", "email", user_data={"email": "test@example.com"})
        ('email', 'email', 1.0)
    """
    # Validate field names are non-empty strings
    if not user_field or not isinstance(user_field, str):
        raise ValidationError("user_field must be a non-empty string")

    if not form_field or not isinstance(form_field, str):
        raise ValidationError("form_field must be a non-empty string")

    # Validate confidence score
    if not isinstance(confidence, (int, float)):
        raise ValidationError(f"confidence must be a number, got {type(confidence).__name__}")

    if not 0.0 <= confidence <= 1.0:
        raise FieldMappingError(
            f"Confidence score must be between 0.0 and 1.0, got {confidence}",
            user_field=user_field,
            form_field=form_field,
        )

    # Validate user field exists in user data if provided
    if user_data is not None:
        if not isinstance(user_data, dict):
            raise ValidationError(f"user_data must be a dictionary, got {type(user_data).__name__}")
        if user_field not in user_data:
            raise FieldMappingError(
                f"User field '{user_field}' not found in user data",
                user_field=user_field,
                form_field=form_field,
            )

    # Validate form field exists in form fields list if provided
    if form_fields is not None:
        if not isinstance(form_fields, list):
            raise ValidationError(f"form_fields must be a list, got {type(form_fields).__name__}")
        if form_field not in form_fields:
            raise FieldMappingError(
                f"Form field '{form_field}' not found in form fields",
                user_field=user_field,
                form_field=form_field,
            )

    return user_field, form_field, confidence


# Helper functions for type-specific validation


def _is_empty(value: Any) -> bool:
    """Check if a value is empty (None, empty string, etc.)."""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict, tuple)):
        return len(value) == 0
    return False


def _validate_text(value: Any, field_name: str) -> str:
    """Validate and convert value to text."""
    if isinstance(value, str):
        return value
    # Try to convert to string
    try:
        return str(value)
    except Exception as e:
        raise DataValidationError(
            f"Cannot convert value to text: {e}",
            field_name=field_name,
            expected_type="text",
            actual_value=value,
        ) from e


def _validate_boolean(value: Any, field_name: str) -> bool:
    """Validate and convert value to boolean."""
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        lower_val = value.lower().strip()
        if lower_val in ("true", "yes", "1", "on"):
            return True
        elif lower_val in ("false", "no", "0", "off", ""):
            return False
        else:
            raise DataValidationError(
                f"Cannot convert string '{value}' to boolean",
                field_name=field_name,
                expected_type="boolean",
                actual_value=value,
            )

    if isinstance(value, (int, float)):
        return bool(value)

    raise DataValidationError(
        f"Cannot convert {type(value).__name__} to boolean",
        field_name=field_name,
        expected_type="boolean",
        actual_value=value,
    )


def _validate_number(
    value: Any,
    field_name: str,
    min_value: float | None = None,
    max_value: float | None = None,
) -> float:
    """Validate and convert value to number, with optional range check."""
    # Convert to float
    if isinstance(value, (int, float)):
        num_value = float(value)
    elif isinstance(value, str):
        try:
            cleaned = value.strip().replace(",", "").replace(" ", "")
            num_value = float(cleaned)
        except ValueError as e:
            raise DataValidationError(
                f"Cannot convert string '{value}' to number: {e}",
                field_name=field_name,
                expected_type="number",
                actual_value=value,
            ) from e
    else:
        raise DataValidationError(
            f"Cannot convert {type(value).__name__} to number",
            field_name=field_name,
            expected_type="number",
            actual_value=value,
        )

    # Check range constraints
    if min_value is not None and num_value < min_value:
        raise DataValidationError(
            f"Value {num_value} is below minimum {min_value}",
            field_name=field_name,
            expected_type="number",
            actual_value=value,
        )

    if max_value is not None and num_value > max_value:
        raise DataValidationError(
            f"Value {num_value} exceeds maximum {max_value}",
            field_name=field_name,
            expected_type="number",
            actual_value=value,
        )

    return num_value


def _validate_date(value: Any, field_name: str) -> str:
    """Validate date value (basic string validation for now)."""
    # For now, just validate it's a non-empty string
    # In future, could add date format validation
    if isinstance(value, str):
        if value.strip():
            return value.strip()
        raise DataValidationError(
            "Date value cannot be empty",
            field_name=field_name,
            expected_type="date",
            actual_value=value,
        )

    # Try to convert to string
    try:
        str_value = str(value)
        if str_value.strip():
            return str_value.strip()
        raise DataValidationError(
            "Date value cannot be empty",
            field_name=field_name,
            expected_type="date",
            actual_value=value,
        )
    except Exception as e:
        raise DataValidationError(
            f"Cannot convert value to date string: {e}",
            field_name=field_name,
            expected_type="date",
            actual_value=value,
        ) from e


def _validate_choice(
    value: Any,
    field_name: str,
    options: list[str] | None = None,
) -> str:
    """Validate choice value against allowed options."""
    # Convert to string
    if isinstance(value, str):
        str_value = value
    else:
        str_value = str(value)

    # If no options specified, just return the string value
    if options is None:
        return str_value

    # Check if value is in allowed options
    if str_value not in options:
        raise DataValidationError(
            f"Value '{str_value}' is not in allowed options: {', '.join(options)}",
            field_name=field_name,
            expected_type="choice",
            actual_value=value,
        )

    return str_value
