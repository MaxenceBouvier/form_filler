"""Dependency injection container."""

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


class ServiceContainer:
    """Simple dependency injection container."""

    def __init__(self):
        """Initialize the container."""
        self._services: dict[type | str, Any] = {}
        self._factories: dict[type | str, Callable] = {}

    def register(self, interface: type | str, implementation: Any) -> None:
        """Register a service implementation.

        Args:
            interface: Interface type or string identifier.
            implementation: Service implementation instance.
        """
        self._services[interface] = implementation

    def register_factory(self, interface: type | str, factory: Callable) -> None:
        """Register a factory function for lazy initialization.

        Args:
            interface: Interface type or string identifier.
            factory: Factory function that creates the service.
        """
        self._factories[interface] = factory

    def resolve(self, interface: type | str) -> Any:
        """Resolve a service by interface.

        Args:
            interface: Interface type or string identifier.

        Returns:
            The service implementation.

        Raises:
            ValueError: If no service is registered for the interface.
        """
        # Check if service is already instantiated
        if interface in self._services:
            return self._services[interface]

        # Check if factory exists
        if interface in self._factories:
            service = self._factories[interface]()
            self._services[interface] = service
            return service

        raise ValueError(f"No service registered for {interface}")

    def has(self, interface: type | str) -> bool:
        """Check if a service is registered.

        Args:
            interface: Interface type or string identifier.

        Returns:
            True if the service is registered, False otherwise.
        """
        return interface in self._services or interface in self._factories


# Global container instance
container = ServiceContainer()


def setup_container():
    """Setup the dependency injection container with default services."""
    from form_filler.application.field_categorizer import RuleBasedFieldCategorizer
    from form_filler.domain.interfaces import FieldCategorizer, PDFProcessor
    from form_filler.infrastructure.pdf.pypdfform_adapter import PyPDFFormAdapter
    from form_filler.infrastructure.persistence.json_repository import (
        JSONRepository,
    )
    from form_filler.infrastructure.persistence.yaml_repository import (
        YAMLRepository,
    )

    # Register services
    container.register(PDFProcessor, PyPDFFormAdapter())
    container.register_factory(FieldCategorizer, RuleBasedFieldCategorizer)

    # Register repositories
    container.register("json_repository", JSONRepository())

    # Register YAML repository if PyYAML is available
    try:
        container.register("yaml_repository", YAMLRepository())
    except RuntimeError as e:
        logger.info("YAML repository not available: %s", e)
        # YAML support is optional, continue without it
