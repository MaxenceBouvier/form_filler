"""YAML file repository implementation."""

from pathlib import Path
from typing import Any

from form_filler.domain.exceptions import DataRepositoryError


class YAMLRepository:
    """YAML file repository implementation."""

    def __init__(self):
        """Initialize the YAML repository."""
        self._yaml: Any | None = None
        self._ensure_yaml_available()

    def _ensure_yaml_available(self):
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
