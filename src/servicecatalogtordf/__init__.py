"""Servicecatalog package.

Modules:
    service

Example:
    >>> from datacatalogtordf import Catalog
    >>> from servicecatalogtordf import PublicOrganization, Service
    >>>
    >>> # Create catalog object
    >>> catalog = Catalog()
    >>> catalog.identifier = "http://example.com/catalogs/1"
    >>> catalog.title = {"en": "A service catalog"}
    >>> catalog.publisher = "https://example.com/publishers/1"
    >>>
    >>> # Create a service:
    >>> service = Service("http://example.com/services/1")
    >>> service.title = {"nb": "inntektsAPI", "en": "incomeAPI"}
    >>> # Create a public organization:
    >>> public_organization = PublicOrganization("https://example.com/publishers/1")
    >>> # Add it to the service:
    >>> service.has_competent_authority = public_organization
    >>> #
    >>> # Add service to catalog:
    >>> catalog.services.append(service)

    >>> # Get rdf representation in turtle (default)
    >>> bool(catalog.to_rdf())
"""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .event import Event
from .evidence import Evidence
from .legal_resource import LegalResource, ResourceType
from .public_organization import PublicOrganization
from .rule import Rule
from .service import Service
