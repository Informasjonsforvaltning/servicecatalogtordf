"""Module for mapping a service to rdf.

This module contains methods for mapping a service object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-service>`__

Example:
    >>> from servicecatalogtordf import Service
    >>>
    >>> service = Service()
    >>> service.identifier = "http://example.com/services/1"
    >>> service.title = {"en": "Title of service"}
    >>>
    >>> bool(service.to_rdf())
    True
"""
from __future__ import annotations

from typing import Optional

from datacatalogtordf import URI
from rdflib import Graph, Literal, Namespace, RDF, URIRef


DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CPSV = Namespace("http://purl.org/vocab/cpsv#")


class Service:
    """A class representing a cpsv:PublicService.

    Ref: `cpsv:PublicService <https://data.norge.no/specification/dcat-ap-no/#klasse-offentlig-tjeneste>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the service
        title (dict):  A name given to the item. key is langauge code.
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_title",
    )

    # Types
    _g: Graph
    _identifier: URI
    _title: dict

    def __init__(self) -> None:
        """Inits an object with default values."""

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
        self._g.add((URIRef(self.identifier), RDF.type, CPSV.PublicService))

        self._title_to_graph()

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
