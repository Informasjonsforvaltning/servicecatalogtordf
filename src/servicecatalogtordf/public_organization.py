"""Module for mapping a PublicOrganization to rdf.

This module contains methods for mapping a PublicOrganization object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#OffentligOrganisasjon>`_ # noqa

Example:
    >>> from datacatalogtordf import Location
    >>> from servicecatalogtordf import PublicOrganization
    >>>
    >>> # Create the public organization:
    >>> public_organization = PublicOrganization("http://example.com/public-organizations/1")
    >>> public_organization.title = {"en": "Title of public organization"}
    >>> # Create and add a location to the spatial_coverage property:
    >>> location = Location()
    >>> location.identifier = "http://publications.europa.eu/resource/authority/country/NOR"
    >>> public_organization.spatial_coverage = location
    >>>
    >>> bool(public_organization.to_rdf())
    True
"""
from __future__ import annotations

from typing import Optional

from datacatalogtordf import Location, URI
from rdflib import Graph, Literal, Namespace, RDF, SKOS, URIRef
from skolemizer import Skolemizer


DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CV = Namespace("http://data.europa.eu/m8g/")


class PublicOrganization:
    """A class representing a cv:PublicOrganization.

    Ref: `cv:PublicOrganization <https://data.norge.no/specification/dcat-ap-no/#OffentligOrganisasjon>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the organization
        spatial_coverage (Location): The geographical area covered by the organization.
        dct_identifier (str):  A formal identifier of the organization.
        pref_label (dict): The preferred name given to the organization. key is language code.
        title (dict):  A name given to the organization. key is language code.
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_spatial_coverage",
        "_pref_label",
        "_dct_identifier",
        "_title",
    )

    # Types
    _g: Graph
    _identifier: URI
    _spatial_coverage: Location
    _pref_label: dict
    _dct_identifier: str
    _title: dict

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        self.identifier = identifier

    @property
    def identifier(self: PublicOrganization) -> Optional[str]:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: PublicOrganization, identifier: Optional[str]) -> None:
        if identifier:
            self._identifier = URI(identifier)

    @property
    def title(self: PublicOrganization) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self: PublicOrganization, title: dict) -> None:
        self._title = title

    @property
    def dct_identifier(self: PublicOrganization) -> str:
        """dct_identifier attribute."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: PublicOrganization, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def pref_label(self: PublicOrganization) -> dict:
        """pref_label attribute."""
        return self._pref_label

    @pref_label.setter
    def pref_label(self: PublicOrganization, pref_label: dict) -> None:
        self._pref_label = pref_label

    @property
    def spatial_coverage(self: PublicOrganization) -> Location:
        """spatial_coverage attribute."""
        return self._spatial_coverage

    @spatial_coverage.setter
    def spatial_coverage(self: PublicOrganization, spatial_coverage: Location) -> None:
        self._spatial_coverage = spatial_coverage

    # -

    def to_rdf(
        self: PublicOrganization,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> bytes:
        """Maps the public_organization to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format (str): a valid format.
            encoding (str): the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: PublicOrganization,
    ) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)
        self._g.bind("cv", CV)
        self._g.add((URIRef(self.identifier), RDF.type, CV.PublicOrganization))

        self._title_to_graph()
        self._dct_identifier_to_graph()
        self._pref_label_to_graph()
        self._spatial_coverage_to_graph()

        return self._g

    # -
    def _title_to_graph(self: PublicOrganization) -> None:
        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

    def _dct_identifier_to_graph(self: PublicOrganization) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier),
                )
            )

    def _pref_label_to_graph(self: PublicOrganization) -> None:
        if getattr(self, "pref_label", None):
            for key in self.pref_label:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        SKOS.prefLabel,
                        Literal(self.pref_label[key], lang=key),
                    )
                )

    def _spatial_coverage_to_graph(self: PublicOrganization) -> None:
        if getattr(self, "spatial_coverage", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.spatial,
                    URIRef(self.spatial_coverage.identifier),
                )
            )
