"""Module for mapping a service to rdf.

This module contains methods for mapping a service object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#OffentligTjeneste>`_

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

from .event import Event
from .evidence import Evidence
from .legal_resource import LegalResource
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
        has_legal_resources (List[LegalResource]): a legal resource that the service is related to
        processing_time (str): the (estimated) time needed for executing a Public
        has_input (List[Evidence]): links the Service to one or more instances of the Evidence class
        is_grouped_by (List[Event]): links the Public Service to the Event class
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_title",
        "_description",
        "_dct_identifier",
        "_has_competent_authority",
        "_follows",
        "_has_legal_resources",
        "_processing_time",
        "_has_input",
        "_is_grouped_by",
    )

    # Types
    _g: Graph
    _identifier: URI
    _title: dict
    _description: dict
    _dct_identifier: str
    _has_competent_authority: PublicOrganization
    _follows: List[Rule]
    _has_legal_resources: List[LegalResource]
    _processing_time: str
    _has_input: List[Evidence]
    _is_grouped_by: List[Event]

    def __init__(self, identifier: str) -> None:
        """Inits an object with default values."""
        self.identifier = identifier
        self.follows = list()
        self.has_legal_resources = list()
        self.has_input = list()
        self.is_grouped_by = list()

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

    @property
    def has_legal_resources(self: Service) -> List[LegalResource]:
        """Follows attribute."""
        return self._has_legal_resources

    @has_legal_resources.setter
    def has_legal_resources(
        self: Service, has_legal_resources: List[LegalResource]
    ) -> None:
        self._has_legal_resources = has_legal_resources

    @property
    def processing_time(self: Service) -> str:
        """processing_time attribute."""
        return self._processing_time

    @processing_time.setter
    def processing_time(self: Service, processing_time: str) -> None:
        self._processing_time = processing_time

    @property
    def has_input(self: Service) -> List[Evidence]:
        """Has_input attribute."""
        return self._has_input

    @has_input.setter
    def has_input(self: Service, has_input: List[Evidence]) -> None:
        self._has_input = has_input

    @property
    def is_grouped_by(self: Service) -> List[Event]:
        """Has_input attribute."""
        return self._is_grouped_by

    @is_grouped_by.setter
    def is_grouped_by(self: Service, is_grouped_by: List[Event]) -> None:
        self._is_grouped_by = is_grouped_by

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
        self._has_legal_resources_to_graph()
        self._processing_time_to_graph()
        self._has_input_to_graph()
        self._is_grouped_by_to_graph()

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

    def _has_legal_resources_to_graph(self: Service) -> None:
        if getattr(self, "has_legal_resources", None):
            for _legal_resource in self.has_legal_resources:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        CV.hasLegalResource,
                        URIRef(_legal_resource.identifier),
                    )
                )

    def _processing_time_to_graph(self: Service) -> None:
        if getattr(self, "processing_time", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    CV.processingTime,
                    Literal(self.processing_time, datatype=XSD.duration),
                )
            )

    def _has_input_to_graph(self: Service) -> None:
        if getattr(self, "has_input", None):
            for _evidence in self.has_input:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        CPSV.hasInput,
                        URIRef(_evidence.identifier),
                    )
                )

    def _is_grouped_by_to_graph(self: Service) -> None:
        if getattr(self, "is_grouped_by", None):
            for _event in self.is_grouped_by:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        CV.isGroupedBy,
                        URIRef(_event.identifier),
                    )
                )
