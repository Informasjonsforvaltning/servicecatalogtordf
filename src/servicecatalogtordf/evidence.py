"""Module for mapping a Evidence to rdf.

This module contains methods for mapping a Evidence object to rdf
according to the `cpsv-ap specification <https://ec.europa.eu/isa2/solutions/core-public-service-vocabulary-application-profile-cpsv-ap_en>`_ # noqa

Example:
    >>> from servicecatalogtordf import Evidence
    >>>
    >>> # Create the evidence:
    >>> evidence = Evidence("http://example.com/evidences/1")
    >>> evidence.dct_identifier = "1"
    >>> evidence.name = {"nb": "Mitt bevis"}
    >>>
    >>> bool(evidence.to_rdf())
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


class Evidence:
    """A class representing a cpsv:Evidence.

    Ref: `cpsv:Evidence <https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/core-public-service-vocabulary-application-profile>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the evidence
        dct_identifier (str):  A formal identifier of the evidence.
        name (dict): The official name of the piece of evidence. key is language code.
        description (dict): A description given to the evidence. key is language code.
        type (URI): the type of evidence as described in a controlled vocabulary.
        related_documentation (List[URI]): References to other information resources
        languages (List[URI]): A list of languages in which the evidence must be provided

    """

    __slots__ = (
        "_g",
        "_identifier",
        "_dct_identifier",
        "_name",
        "_description",
        "_type",
        "_related_documentation",
        "_languages",
    )

    # Types
    _g: Graph
    _identifier: URI
    _dct_identifier: str
    _name: dict
    _description: dict
    _type: URI
    _related_documentation: List[URI]
    _languages: List[URI]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        self.identifier = identifier
        self.related_documentation = list()
        self.languages = list()

    @property
    def identifier(self: Evidence) -> Optional[str]:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Evidence, identifier: Optional[str]) -> None:
        if identifier:
            self._identifier = URI(identifier)

    @property
    def name(self: Evidence) -> dict:
        """Title attribute."""
        return self._name

    @name.setter
    def name(self: Evidence, name: dict) -> None:
        self._name = name

    @property
    def dct_identifier(self: Evidence) -> str:
        """dct_identifier attribute."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: Evidence, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def description(self: Evidence) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self: Evidence, description: dict) -> None:
        self._description = description

    @property
    def type(self: Evidence) -> str:
        """Types attribute."""
        return self._type

    @type.setter
    def type(self: Evidence, type: str) -> None:
        self._type = URI(type)

    @property
    def related_documentation(self: Evidence) -> List[str]:
        """Implements attribute."""
        return self._related_documentation

    @related_documentation.setter
    def related_documentation(self: Evidence, related_documentation: List[str]) -> None:
        self._related_documentation = related_documentation

    @property
    def languages(self: Evidence) -> List[str]:
        """Languages attribute."""
        return self._languages

    @languages.setter
    def languages(self: Evidence, languages: List[str]) -> None:
        self._languages = languages

    # -

    def to_rdf(
        self: Evidence,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> bytes:
        """Maps the evidence to rdf.

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
        self: Evidence,
    ) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)
        self._g.bind("cpsv", CPSV)
        self._g.bind("foaf", FOAF)

        self._g.add((URIRef(self.identifier), RDF.type, CPSV.Evidence))

        self._dct_identifier_to_graph()
        self._name_to_graph()
        self._description_to_graph()
        self._type_to_graph()
        self._related_documentation_to_graph()
        self._languages_to_graph()

        return self._g

    # -
    def _dct_identifier_to_graph(self: Evidence) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier),
                )
            )

    def _name_to_graph(self: Evidence) -> None:
        if getattr(self, "name", None):
            for key in self.name:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.name[key], lang=key),
                    )
                )

    def _description_to_graph(self: Evidence) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _type_to_graph(self: Evidence) -> None:
        if getattr(self, "type", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.type,
                    URIRef(self._type),
                )
            )

    def _related_documentation_to_graph(self: Evidence) -> None:
        if getattr(self, "related_documentation", None):
            for _page in self.related_documentation:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        FOAF.page,
                        URIRef(_page),
                    )
                )

    def _languages_to_graph(self: Evidence) -> None:
        if getattr(self, "languages", None):
            for _language in self.languages:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.language,
                        URIRef(_language),
                    )
                )
