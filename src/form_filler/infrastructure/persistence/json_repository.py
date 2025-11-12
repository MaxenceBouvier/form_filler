"""JSON file repository implementation.

This module provides a JSON-based implementation of the DataRepository protocol.
It handles saving and loading structured data in JSON format with UTF-8 encoding.
"""

import json
from pathlib import Path
from typing import Any

from form_filler.domain.exceptions import DataRepositoryError


class JSONRepository:
    """JSON file repository implementing DataRepository protocol.

    This class provides JSON-based data persistence with support for:
    - UTF-8 encoding
    - Configurable formatting (indentation, ASCII escaping)
    - Automatic directory creation
    - User profile listing

    Attributes:
        ensure_ascii: Whether to escape non-ASCII characters in output.
        indent: Number of spaces for indentation in output files.

    Examples:
        >>> from pathlib import Path
        >>> repo = JSONRepository(indent=2)
        >>> repo.save({"name": "John"}, Path("user.json"))
        >>> data = repo.load(Path("user.json"))
        >>> data["name"]
        'John'
    """

    def __init__(self, ensure_ascii: bool = False, indent: int = 2):
        """Initialize the JSON repository.

        Args:
            ensure_ascii: If True, escape non-ASCII characters.
                         If False (default), preserve Unicode characters.
            indent: Number of spaces for indentation (default: 2).
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

        Examples:
            >>> repo = JSONRepository()
            >>> repo.save({"key": "value"}, Path("data.json"))
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
            FileNotFoundError: If path doesn't exist.

        Examples:
            >>> repo = JSONRepository()
            >>> data = repo.load(Path("user.json"))
            >>> isinstance(data, dict)
            True
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

    def exists(self, path: Path) -> bool:
        """Check if data exists at the specified path.

        Args:
            path: Path to check.

        Returns:
            True if the file exists, False otherwise.

        Examples:
            >>> repo = JSONRepository()
            >>> repo.exists(Path("user.json"))
            True
            >>> repo.exists(Path("nonexistent.json"))
            False
        """
        return path.exists() and path.is_file()

    def list_profiles(self, directory: Path) -> list[Path]:
        """List all JSON profile files in a directory.

        Args:
            directory: Directory to search for JSON profiles.

        Returns:
            List of paths to JSON files, sorted by modification time (newest first).

        Raises:
            DataRepositoryError: If directory access fails.

        Examples:
            >>> repo = JSONRepository()
            >>> profiles = repo.list_profiles(Path("resources/user_info"))
            >>> all(p.suffix == ".json" for p in profiles)
            True
        """
        try:
            if not directory.exists():
                return []

            if not directory.is_dir():
                raise DataRepositoryError(f"Not a directory: {directory}")

            # Find all JSON files in the directory
            json_files = list(directory.glob("*.json"))

            # Sort by modification time, newest first
            json_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            return json_files

        except Exception as e:
            raise DataRepositoryError(f"Failed to list profiles in {directory}: {e}") from e
