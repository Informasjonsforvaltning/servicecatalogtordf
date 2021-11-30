"""Test cases for the rule module."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import LegalResource, Rule
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_rule_with_title() -> None:
    """It returns a rule graph with dct:title isomorphic to spec."""
    rule = Rule("http://example.com/rules/1")
    rule.title = {
        "en": "Rule 1",
        "nb": "Regel 1",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/rules/1> a cpsv:Rule ;
        dct:title   "Rule 1"@en, "Regel 1"@nb ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_with_dct_identifier() -> None:
    """It returns a rule graph with dct:identifier isomorphic to spec."""
    rule = Rule("http://example.com/rules/1")
    rule.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/rules/1> a cpsv:Rule ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
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
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a cpsv:Rule ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_with_description() -> None:
    """It returns a rule graph with dct:description isomorphic to spec."""
    rule = Rule("http://example.com/rules/1")
    rule.description = {
        "en": "Rule 1 description",
        "nb": "Regel 1 beskrivelse",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/rules/1> a cpsv:Rule ;
        dct:description  "Rule 1 description"@en ,
                         "Regel 1 beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_with_implements() -> None:
    """It returns a rule graph with cpsv:implements isomorphic to spec."""
    rule = Rule("http://example.com/rules/1")
    a_legal_resource = LegalResource("https://example.com/legalresources/1")
    rule.implements.append(a_legal_resource)
    another_legal_resource = LegalResource("https://example.com/legalresources/2")
    rule.implements.append(another_legal_resource)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/rules/1> a cpsv:Rule ;
        cpsv:implements  <https://example.com/legalresources/1> ,
                         <https://example.com/legalresources/2> ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_with_languages() -> None:
    """It returns a rule graph with dct:language isomorphic to spec."""
    rule = Rule("http://example.com/rules/1")
    nob = "http://publications.europa.eu/resource/authority/language/NOB"
    eng = "http://publications.europa.eu/resource/authority/language/ENG"
    rule.languages.append(nob)
    rule.languages.append(eng)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/rules/1> a cpsv:Rule ;
        dct:language  <http://publications.europa.eu/resource/authority/language/NOB> ,
                      <http://publications.europa.eu/resource/authority/language/ENG> ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_rule_with_types() -> None:
    """It returns a rule graph with dct:type isomorphic to spec."""
    rule = Rule("http://example.com/rules/1")
    a_type = "http://vocabulary.com/types/1"
    another_type = "http://vocabulary.com/types/2"
    rule.types.append(a_type)
    rule.types.append(another_type)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/rules/1> a cpsv:Rule ;
        dct:type  <http://vocabulary.com/types/1> ,
                  <http://vocabulary.com/types/2> ;
    .
    """
    g1 = Graph().parse(data=rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
