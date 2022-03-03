"""Module for mapping a CriterionRequirement to rdf.

This module contains methods for mapping a CriterionRequirement object to rdf
according to the
`cpsv-ap-no specification <https://data.norge.no/specification/cpsv-ap-no>`_ # noqa

Example:
    >>> from servicecatalogtordf import CriterionRequirement
    >>>
    >>> # Create the criterion requirement:
    >>> criterion_requirement = CriterionRequirement("http://example.com/criterion-requirement/1")
    >>> criterion_requirement.identifier = "http://example.com/criterion-requirement/1"
    >>> criterion_requirement.title = {"en": "Title of criterion requirement"}
    >>>
    >>> bool(criterion_requirement.to_rdf())
    True
"""
from __future__ import annotations

from typing import List, Optional, Union

from datacatalogtordf import URI
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from skolemizer import Skolemizer

DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CPSV = Namespace("http://purl.org/vocab/cpsv#")
CV = Namespace("http://data.europa.eu/m8g/")


class CriterionRequirement:
    """A class representing a cv:CriterionRequirement.

    Ref: `cv:CriterionRequirement <https://data.norge.no/specification/dcat-ap-no/#Regel>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the criterion requirement
        dct_identifier (str):  A formal identifier of the criterion requirement.
        title (dict):  A name given to the criterion requirement. key is language code.
        types (List[URI]): Links to concepts in a vocabulary describing types of Criterion Requirements.
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_dct_identifier",
        "_title",
        "_types",
    )

    # Types
    _g: Graph
    _identifier: URI
    _dct_identifier: str
    _title: dict
    _types: List[URI]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        self.types = list()

    @property
    def identifier(self: CriterionRequirement) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: CriterionRequirement, identifier: str) -> None:
        if identifier:
            self._identifier = URI(identifier)

    @property
    def title(self: CriterionRequirement) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self: CriterionRequirement, title: dict) -> None:
        self._title = title

    @property
    def dct_identifier(self: CriterionRequirement) -> str:
        """dct_identifier attribute."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: CriterionRequirement, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def types(self: CriterionRequirement) -> List[str]:
        """Types attribute."""
        return self._types

    @types.setter
    def types(self: CriterionRequirement, types: List[str]) -> None:
        self._types = types

    # -

    def to_rdf(
        self: CriterionRequirement,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> Union[bytes, str]:
        """Maps the criterion requirement to rdf.

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
        self: CriterionRequirement,
    ) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)
        self._g.bind("cpsv", CPSV)
        self._g.bind("cv", CV)
        self._g.add((URIRef(self.identifier), RDF.type, CV.CriterionRequirement))

        self._title_to_graph()
        self._dct_identifier_to_graph()
        self._title_to_graph()
        self._types_to_graph()

        return self._g

    # -
    def _title_to_graph(self: CriterionRequirement) -> None:
        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

    def _dct_identifier_to_graph(self: CriterionRequirement) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier, datatype=XSD.anyURI),
                )
            )

    def _types_to_graph(self: CriterionRequirement) -> None:
        if getattr(self, "types", None):
            for _type in self.types:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.type,
                        URIRef(_type),
                    )
                )
