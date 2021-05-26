"""Module for mapping a Event to rdf.

This module contains methods for mapping a Event object to rdf
according to the `cpsv-ap specification <https://ec.europa.eu/isa2/solutions/core-public-service-vocabulary-application-profile-cpsv-ap_en>`_ # noqa

Example:
    >>> from servicecatalogtordf import Event
    >>>
    >>> # Create the event:
    >>> event = Event("http://example.com/events/1")
    >>> event.dct_identifier = "1"
    >>> event.name = {"nb": "Mitt bevis"}
    >>>
    >>> bool(event.to_rdf())
    True
"""
from __future__ import annotations

from typing import List, Optional

from datacatalogtordf import URI
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from skolemizer import Skolemizer


DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CPSV = Namespace("http://purl.org/vocab/cpsv#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class Event:
    """A class representing a cpsv:Event.

    Ref: `cpsv:Event <https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/core-public-service-vocabulary-application-profile>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the event
        dct_identifier (str):  A formal identifier of the event.
        name (dict): The official name of the piece of event. key is language code.
        description (dict): A description given to the event. key is language code.
        type (URI): the type of event as described in a controlled vocabulary.
        related_service (List[URI]): References to other information resources

    """

    __slots__ = (
        "_g",
        "_identifier",
        "_dct_identifier",
        "_name",
        "_description",
        "_type",
        "_related_service",
    )

    # Types
    _g: Graph
    _identifier: URI
    _dct_identifier: str
    _name: dict
    _description: dict
    _type: URI
    _related_service: List[URI]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        self.identifier = identifier
        self.related_service = list()

    @property
    def identifier(self: Event) -> Optional[str]:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Event, identifier: Optional[str]) -> None:
        if identifier:
            self._identifier = URI(identifier)

    @property
    def name(self: Event) -> dict:
        """Title attribute."""
        return self._name

    @name.setter
    def name(self: Event, name: dict) -> None:
        self._name = name

    @property
    def dct_identifier(self: Event) -> str:
        """dct_identifier attribute."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: Event, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def description(self: Event) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self: Event, description: dict) -> None:
        self._description = description

    @property
    def type(self: Event) -> str:
        """Types attribute."""
        return self._type

    @type.setter
    def type(self: Event, type: str) -> None:
        self._type = URI(type)

    @property
    def related_service(self: Event) -> List[str]:
        """Related_service attribute."""
        return self._related_service

    @related_service.setter
    def related_service(self: Event, related_service: List[str]) -> None:
        self._related_service = related_service

    # -

    def to_rdf(
        self: Event,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> bytes:
        """Maps the event to rdf.

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
        self: Event,
    ) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)
        self._g.bind("cpsv", CPSV)

        self._g.add((URIRef(self.identifier), RDF.type, CPSV.Event))

        self._dct_identifier_to_graph()
        self._name_to_graph()
        self._description_to_graph()
        self._type_to_graph()
        self._related_service_to_graph()

        return self._g

    # -
    def _dct_identifier_to_graph(self: Event) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier),
                )
            )

    def _name_to_graph(self: Event) -> None:
        if getattr(self, "name", None):
            for key in self.name:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.name[key], lang=key),
                    )
                )

    def _description_to_graph(self: Event) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _type_to_graph(self: Event) -> None:
        if getattr(self, "type", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.type,
                    URIRef(self._type),
                )
            )

    def _related_service_to_graph(self: Event) -> None:
        if getattr(self, "related_service", None):
            for _service in self.related_service:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.relation,
                        URIRef(_service),
                    )
                )
