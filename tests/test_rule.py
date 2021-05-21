"""Test cases for the rule module."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import Rule
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_rule_with_title() -> None:
    """It returns a rule graph with dct:title isomorphic to spec."""
    rule = Rule("http://example.com/public-organizations/1")
    rule.title = {
        "en": "Rule 1",
        "nb": "Regel 1",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/public-organizations/1> a cv:Rule ;
        dct:title   "Rule 1"@en, "Regel 1"@nb ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_with_dct_identifier() -> None:
    """It returns a rule graph with dct:identifier isomorphic to spec."""
    rule = Rule("http://example.com/public-organizations/1")
    rule.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/public-organizations/1> a cv:Rule ;
        dct:identifier   "https://unique.uri.com" ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_as_blank_node(
    mocker: MockFixture,
) -> None:
    """It returns a rule graph with skolem uri isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    rule = Rule()
    rule.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a cv:Rule ;
        dct:identifier   "https://unique.uri.com" ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_with_description() -> None:
    """It returns a rule graph with dct:description isomorphic to spec."""
    rule = Rule("http://example.com/public-organizations/1")
    rule.description = {
        "en": "Rule 1 description",
        "nb": "Regel 1 beskrivelse",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/public-organizations/1> a cv:Rule ;
        dct:description  "Rule 1 description"@en ,
                         "Regel 1 beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
