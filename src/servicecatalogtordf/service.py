"""Module for mapping a service to rdf.

This module contains methods for mapping a service object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#OffentligTjeneste>`__

Example:
    >>> from servicecatalogtordf import Service
    >>>
    >>> service = Service("http://example.com/services/1")
    >>> service.title = {"en": "Title of service"}
    >>>
    >>> bool(service.to_rdf())
    True
"""
from __future__ import annotations

from typing import List, Optional

from datacatalogtordf import URI
from rdflib import Graph, Literal, Namespace, RDF, URIRef

from .public_organization import PublicOrganization
from .rule import Rule

DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CPSV = Namespace("http://purl.org/vocab/cpsv#")
CV = Namespace("http://data.europa.eu/m8g/")


class Service:
    """A class representing a cpsv:PublicService.

    Ref: `cpsv:PublicService <https://data.norge.no/specification/dcat-ap-no/#klasse-offentlig-tjeneste>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the service
        title (dict):  A name given to the service. key is langauge code.
        description (dict):  A description given to the service. key is langauge code.
        dct_identifier (str):  A formal identifier of the service.
        has_competent_authority (PublicOrganization): the organization responsible for the service
        follows (List[Rule]): the rules under which the service is offered
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_title",
        "_description",
        "_dct_identifier",
        "_has_competent_authority",
        "_follows",
    )

    # Types
    _g: Graph
    _identifier: URI
    _title: dict
    _description: dict
    _dct_identifier: str
    _has_competent_authority: PublicOrganization
    _follows: List[Rule]

    def __init__(self, identifier: str) -> None:
        """Inits an object with default values."""
        self.identifier = identifier
        self.follows = list()

    @property
    def identifier(self: Service) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Service, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def title(self: Service) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self: Service, title: dict) -> None:
        self._title = title

    @property
    def description(self: Service) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self: Service, description: dict) -> None:
        self._description = description

    @property
    def dct_identifier(self: Service) -> str:
        """Dct_identifier attribute."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: Service, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def has_competent_authority(self: Service) -> PublicOrganization:
        """Has_competent_authority attribute."""
        return self._has_competent_authority

    @has_competent_authority.setter
    def has_competent_authority(
        self: Service, has_competent_authority: PublicOrganization
    ) -> None:
        self._has_competent_authority = has_competent_authority

    @property
    def follows(self: Service) -> List[Rule]:
        """Follows attribute."""
        return self._follows

    @follows.setter
    def follows(self: Service, follows: List[Rule]) -> None:
        self._follows = follows

    # -

    def to_rdf(
        self: Service,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> bytes:
        """Maps the service to rdf.

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
        self: Service,
    ) -> Graph:

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)
        self._g.bind("cpsv", CPSV)
        self._g.bind("cv", CV)
        self._g.add((URIRef(self.identifier), RDF.type, CPSV.PublicService))

        self._title_to_graph()
        self._description_to_graph()
        self._dct_identifier_to_graph()
        self._has_competent_authority_to_graph()
        self._follows_to_graph()

        return self._g

    # -
    def _title_to_graph(self: Service) -> None:
        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

    def _description_to_graph(self: Service) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _dct_identifier_to_graph(self: Service) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier),
                )
            )

    def _has_competent_authority_to_graph(self: Service) -> None:
        if getattr(self, "has_competent_authority", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    CV.hasCompetentAuthority,
                    URIRef(self.has_competent_authority.identifier),
                )
            )

    def _follows_to_graph(self: Service) -> None:
        if getattr(self, "follows", None):
            for _rule in self.follows:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        CPSV.follows,
                        URIRef(_rule.identifier),
                    )
                )
