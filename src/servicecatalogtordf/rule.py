"""Module for mapping a Rule to rdf.

This module contains methods for mapping a Rule object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#OffentligOrganisasjon>`__ # noqa

Example:
    >>> from datacatalogtordf import Location
    >>> from servicecatalogtordf import Rule
    >>>
    >>> # Create the rule:
    >>> rule = Rule("http://example.com/rules/1")
    >>> rule.title = {"en": "Title of rule"}
    >>>
    >>> bool(rule.to_rdf())
    True
"""
from __future__ import annotations

from typing import Optional

from datacatalogtordf import URI
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from skolemizer import Skolemizer


DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CV = Namespace("http://data.europa.eu/m8g/")


class Rule:
    """A class representing a cv:Rule.

    Ref: `cv:Rule <https://data.norge.no/specification/dcat-ap-no/#Regel>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the rule
        dct_identifier (str):  A formal identifier of the rule.
        title (dict):  A name given to the rule. key is language code.
        description (dict): A description given to the rule. key is language code.
    """

    __slots__ = ("_g", "_identifier", "_dct_identifier", "_title", "_description")

    # Types
    _g: Graph
    _identifier: URI
    _dct_identifier: str
    _title: dict
    _description: dict

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        self.identifier = identifier

    @property
    def identifier(self: Rule) -> Optional[str]:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Rule, identifier: Optional[str]) -> None:
        if identifier:
            self._identifier = URI(identifier)

    @property
    def title(self: Rule) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self: Rule, title: dict) -> None:
        self._title = title

    @property
    def dct_identifier(self: Rule) -> str:
        """dct_identifier attribute."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: Rule, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def description(self: Rule) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self: Rule, description: dict) -> None:
        self._description = description

    # -

    def to_rdf(
        self: Rule,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> bytes:
        """Maps the rule to rdf.

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
        self: Rule,
    ) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)
        self._g.bind("cv", CV)
        self._g.add((URIRef(self.identifier), RDF.type, CV.Rule))

        self._title_to_graph()
        self._dct_identifier_to_graph()
        self._description_to_graph()

        return self._g

    # -
    def _title_to_graph(self: Rule) -> None:
        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

    def _dct_identifier_to_graph(self: Rule) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier),
                )
            )

    def _description_to_graph(self: Rule) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )
