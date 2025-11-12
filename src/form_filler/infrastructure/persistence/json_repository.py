"""JSON file repository implementation."""

import json
from pathlib import Path
from typing import Any

from form_filler.domain.exceptions import DataRepositoryError


class JSONRepository:
    """JSON file repository implementation."""

    def __init__(self, ensure_ascii: bool = False, indent: int = 2):
        """Initialize the JSON repository.

        Args:
            ensure_ascii: If True, escape non-ASCII characters.
            indent: Number of spaces for indentation.
        """
        self.ensure_ascii = ensure_ascii
        self.indent = indent

    def save(self, data: dict[str, Any], path: Path) -> None:
        """Save data to JSON file.

        Args:
            data: Dictionary to save.
            path: Path where to save the file.

        Raises:
            DataRepositoryError: If save operation fails.
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=self.ensure_ascii, indent=self.indent)
        except Exception as e:
            raise DataRepositoryError(f"Failed to save data to {path}: {e}") from e

    def load(self, path: Path) -> dict[str, Any]:
        """Load data from JSON file.

        Args:
            path: Path to the JSON file.

        Returns:
            Dictionary loaded from the file.

        Raises:
            DataRepositoryError: If load operation fails.
        """
        try:
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")

            with path.open("r", encoding="utf-8") as f:
                result = json.load(f)
                if not isinstance(result, dict):
                    raise DataRepositoryError(f"Invalid JSON format in {path}")
                return result
        except Exception as e:
            raise DataRepositoryError(f"Failed to load data from {path}: {e}") from e
