"""Module for mapping a LegalResource to rdf.

This module contains methods for mapping a LegalResource object to rdf
according to the `dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#RegulativRessurs>`_ # noqa

Example:
    >>> from servicecatalogtordf import LegalResource, ResourceType
    >>>
    >>> # Create the legal_resource:
    >>> legal_resource = LegalResource("http://example.com/legal_resources/1")
    >>> resource_type = ResourceType("http://example.com/types/1")
    >>> legal_resource.types.append(resource_type)
    >>>
    >>> bool(legal_resource.to_rdf())
    True
"""
from __future__ import annotations

from typing import List, Optional

from datacatalogtordf import URI
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from skolemizer import Skolemizer


DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
ELI = Namespace("http://data.europa.eu/eli/ontology#")


class ResourceType:
    """A class representing a eli:ResourceType.

    Ref: `eli:LegalResource <https://data.norge.no/specification/dcat-ap-no/#RegulativRessurs-type>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the legal_resource
    """

    __slots__ = "_identifier"

    # Types
    _identifier: URI

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        self.identifier = identifier

    @property
    def identifier(self: ResourceType) -> Optional[str]:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: ResourceType, identifier: Optional[str]) -> None:
        if identifier:
            self._identifier = URI(identifier)


class LegalResource:
    """A class representing a eli:LegalResource.

    Ref: `eli:LegalResource <https://data.norge.no/specification/dcat-ap-no/#Regel>`_. # noqa

    Attributes:
        identifier (URI): A URI uniquely identifying the legal_resource
        dct_identifier (str):  A formal identifier of the legal_resource.
        types (List[ResourceType]):  A name given to the legal_resource. key is language code.
        description (dict): A description given to the legal_resource. key is language code.
        references (List[URI]): References to other resources
        related (List[LegalResource]): References to other resources
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_dct_identifier",
        "_types",
        "_description",
        "_references",
        "_related",
    )

    # Types
    _g: Graph
    _identifier: URI
    _dct_identifier: str
    _types: List[ResourceType]
    _description: dict
    _references: List[URI]
    _related: List[LegalResource]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        self.identifier = identifier
        self.types = list()
        self.references = list()
        self.related = list()

    @property
    def identifier(self: LegalResource) -> Optional[str]:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: LegalResource, identifier: Optional[str]) -> None:
        if identifier:
            self._identifier = URI(identifier)

    @property
    def types(self: LegalResource) -> List[ResourceType]:
        """Title attribute."""
        return self._types

    @types.setter
    def types(self: LegalResource, types: List[ResourceType]) -> None:
        self._types = types

    @property
    def dct_identifier(self: LegalResource) -> str:
        """dct_identifier attribute."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: LegalResource, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def description(self: LegalResource) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self: LegalResource, description: dict) -> None:
        self._description = description

    @property
    def references(self: LegalResource) -> List[str]:
        """Title attribute."""
        return self._references

    @references.setter
    def references(self: LegalResource, references: List[str]) -> None:
        self._references = references

    @property
    def related(self: LegalResource) -> List[LegalResource]:
        """Title attribute."""
        return self._related

    @related.setter
    def related(self: LegalResource, related: List[LegalResource]) -> None:
        self._related = related

    # -

    def to_rdf(
        self: LegalResource,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> bytes:
        """Maps the legal_resource to rdf.

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
        self: LegalResource,
    ) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)
        self._g.bind("eli", ELI)
        self._g.add((URIRef(self.identifier), RDF.type, ELI.LegalResource))

        self._types_to_graph()
        self._dct_identifier_to_graph()
        self._description_to_graph()
        self._references_to_graph()
        self._related_to_graph()

        return self._g

    # -
    def _types_to_graph(self: LegalResource) -> None:
        if getattr(self, "types", None):
            for _type in self.types:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.type,
                        URIRef(_type.identifier),
                    )
                )

    def _dct_identifier_to_graph(self: LegalResource) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier),
                )
            )

    def _description_to_graph(self: LegalResource) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _references_to_graph(self: LegalResource) -> None:
        if getattr(self, "references", None):
            for _reference in self.references:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        RDFS.seeAlso,
                        URIRef(_reference),
                    )
                )

    def _related_to_graph(self: LegalResource) -> None:
        if getattr(self, "related", None):
            for _legal_resource in self.related:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.relation,
                        URIRef(_legal_resource.identifier),
                    )
                )
