"""Test cases for the legal_resource module."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import LegalResource, ResourceType
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_legal_resource_with_dct_identifier() -> None:
    """It returns a legal_resource graph with dct:identifier isomorphic to spec."""
    legal_resource = LegalResource("http://example.com/legalresources/1")
    legal_resource.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix eli: <http://data.europa.eu/eli/ontology#> .

    <http://example.com/legalresources/1> a eli:LegalResource ;
        dct:identifier   "https://unique.uri.com" ;
    .
    """
    g1 = Graph().parse(data=legal_resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_legal_resource_as_blank_node(
    mocker: MockFixture,
) -> None:
    """It returns a legal_resource graph with skolem uri isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    legal_resource = LegalResource()
    legal_resource.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix eli: <http://data.europa.eu/eli/ontology#> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a eli:LegalResource ;
        dct:identifier   "https://unique.uri.com" ;
    .
    """
    g1 = Graph().parse(data=legal_resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_legal_resource_with_description() -> None:
    """It returns a legal_resource graph with dct:description isomorphic to spec."""
    legal_resource = LegalResource("http://example.com/legalresources/1")
    legal_resource.description = {
        "en": "LegalResource 1 description",
        "nb": "Regulativ ressurs 1 beskrivelse",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix eli: <http://data.europa.eu/eli/ontology#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/legalresources/1> a eli:LegalResource ;
        dct:description  "LegalResource 1 description"@en ,
                         "Regulativ ressurs 1 beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=legal_resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_legal_resource_with_types() -> None:
    """It returns a legal_resource graph with dct:types isomorphic to spec."""
    legal_resource = LegalResource("http://example.com/legalresources/1")
    resource_type = ResourceType("http://example.com/resourcetypes/1")
    legal_resource.types.append(resource_type)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix eli: <http://data.europa.eu/eli/ontology#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/legalresources/1> a eli:LegalResource ;
        dct:type  <http://example.com/resourcetypes/1> ;
    .
    """
    g1 = Graph().parse(data=legal_resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_legal_resource_with_references() -> None:
    """It returns a legal_resource graph with rdfs:seeAlso isomorphic to spec."""
    legal_resource = LegalResource("http://example.com/legalresources/1")
    legal_resource.references.append("https://resources.com/1")
    legal_resource.references.append("https://resources.com/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix eli: <http://data.europa.eu/eli/ontology#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/legalresources/1> a eli:LegalResource ;
        rdfs:seeAlso  <https://resources.com/1> ,
                      <https://resources.com/2> ;
    .
    """
    g1 = Graph().parse(data=legal_resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_legal_resource_with_relations() -> None:
    """It returns a legal_resource graph with dct:related isomorphic to spec."""
    the_legal_resource = LegalResource("http://example.com/legalresources/1")
    # Add related legal resources
    a_legal_resource = LegalResource("http://example.com/legalresources/2")
    the_legal_resource.related.append(a_legal_resource)
    another_legal_resource = LegalResource("http://example.com/legalresources/3")
    the_legal_resource.related.append(another_legal_resource)
    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix eli: <http://data.europa.eu/eli/ontology#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/legalresources/1> a eli:LegalResource ;
        dct:relation  <http://example.com/legalresources/2> ,
                      <http://example.com/legalresources/3> ;
    .
    """
    g1 = Graph().parse(data=the_legal_resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
