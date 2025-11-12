"""YAML file repository implementation.

This module provides a YAML-based implementation of the DataRepository protocol.
It handles saving and loading structured data in YAML format with UTF-8 encoding.
Requires PyYAML to be installed.
"""

from pathlib import Path
from typing import Any

from form_filler.domain.exceptions import DataRepositoryError


class YAMLRepository:
    """YAML file repository implementing DataRepository protocol.

    This class provides YAML-based data persistence with support for:
    - UTF-8 encoding
    - Human-readable formatting
    - Automatic directory creation
    - User profile listing

    Note:
        Requires PyYAML to be installed. Install with: uv pip install pyyaml

    Attributes:
        _yaml: Reference to the yaml module (loaded dynamically).

    Examples:
        >>> from pathlib import Path
        >>> repo = YAMLRepository()
        >>> repo.save({"name": "John"}, Path("user.yaml"))
        >>> data = repo.load(Path("user.yaml"))
        >>> data["name"]
        'John'
    """

    def __init__(self):
        """Initialize the YAML repository.

        Raises:
            RuntimeError: If PyYAML is not installed.
        """
        self._yaml: Any | None = None
        self._ensure_yaml_available()

    def _ensure_yaml_available(self) -> None:
        """Ensure PyYAML is available.

        Raises:
            RuntimeError: If PyYAML is not installed.
        """
        try:
            import yaml

            self._yaml = yaml
        except ImportError as e:
            raise RuntimeError(
                "PyYAML is not installed. "
                "Install it with 'uv pip install pyyaml' to enable YAML support."
            ) from e

    def save(self, data: dict[str, Any], path: Path) -> None:
        """Save data to YAML file.

        Args:
            data: Dictionary to save.
            path: Path where to save the file.

        Raises:
            DataRepositoryError: If save operation fails.

        Examples:
            >>> repo = YAMLRepository()
            >>> repo.save({"key": "value"}, Path("data.yaml"))
        """
        if self._yaml is None:
            raise DataRepositoryError("YAML library not available")

        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            with path.open("w", encoding="utf-8") as f:
                self._yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        except Exception as e:
            raise DataRepositoryError(f"Failed to save data to {path}: {e}") from e

    def load(self, path: Path) -> dict[str, Any]:
        """Load data from YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            Dictionary loaded from the file.

        Raises:
            DataRepositoryError: If load operation fails.
            FileNotFoundError: If path doesn't exist.

        Examples:
            >>> repo = YAMLRepository()
            >>> data = repo.load(Path("user.yaml"))
            >>> isinstance(data, dict)
            True
        """
        if self._yaml is None:
            raise DataRepositoryError("YAML library not available")

        try:
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")

            with path.open("r", encoding="utf-8") as f:
                result = self._yaml.safe_load(f)
                if not isinstance(result, dict):
                    raise DataRepositoryError(f"Invalid YAML format in {path}")
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
            >>> repo = YAMLRepository()
            >>> repo.exists(Path("user.yaml"))
            True
            >>> repo.exists(Path("nonexistent.yaml"))
            False
        """
        return path.exists() and path.is_file()

    def list_profiles(self, directory: Path) -> list[Path]:
        """List all YAML profile files in a directory.

        Args:
            directory: Directory to search for YAML profiles.

        Returns:
            List of paths to YAML files (.yaml and .yml), sorted by modification time (newest first).

        Raises:
            DataRepositoryError: If directory access fails.

        Examples:
            >>> repo = YAMLRepository()
            >>> profiles = repo.list_profiles(Path("resources/user_info"))
            >>> all(p.suffix in [".yaml", ".yml"] for p in profiles)
            True
        """
        try:
            if not directory.exists():
                return []

            if not directory.is_dir():
                raise DataRepositoryError(f"Not a directory: {directory}")

            # Find all YAML files in the directory (.yaml and .yml extensions)
            yaml_files = list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))

            # Sort by modification time, newest first
            yaml_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            return yaml_files

        except Exception as e:
            raise DataRepositoryError(f"Failed to list profiles in {directory}: {e}") from e
