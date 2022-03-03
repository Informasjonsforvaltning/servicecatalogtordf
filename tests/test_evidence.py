"""Test cases for the evidence module."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import Evidence
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_evidence_as_blank_node(
    mocker: MockFixture,
) -> None:
    """It returns a evidence graph with skolem uri isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    evidence = Evidence()
    evidence.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a cpsv:Evidence ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=evidence.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_evidence_with_dct_identifier() -> None:
    """It returns a evidence graph with dct:identifier isomorphic to spec."""
    evidence = Evidence("http://example.com/evidences/1")
    evidence.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/evidences/1> a cpsv:Evidence ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=evidence.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_evidence_with_name() -> None:
    """It returns a evidence graph with dct:title isomorphic to spec."""
    evidence = Evidence("http://example.com/evidences/1")
    evidence.name = {
        "en": "Evidence 1",
        "nb": "Bevis 1",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/evidences/1> a cpsv:Evidence ;
        dct:title  "Evidence 1"@en ,
                   "Bevis 1"@nb ;
    .
    """
    g1 = Graph().parse(data=evidence.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_evidence_with_description() -> None:
    """It returns a evidence graph with dct:description isomorphic to spec."""
    evidence = Evidence("http://example.com/evidences/1")
    evidence.description = {
        "en": "Evidence 1 description",
        "nb": "Bevis 1 beskrivelse",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/evidences/1> a cpsv:Evidence ;
        dct:description  "Evidence 1 description"@en ,
                         "Bevis 1 beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=evidence.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_evidence_with_type() -> None:
    """It returns a evidence graph with dct:type isomorphic to spec."""
    evidence = Evidence("http://example.com/evidences/1")
    evidence.type = "http://example.com/concepts/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/evidences/1> a cpsv:Evidence ;
        dct:type  <http://example.com/concepts/1> ;
    .
    """
    g1 = Graph().parse(data=evidence.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_evidence_with_related_documentation() -> None:
    """It returns a evidence graph with foaf:page isomorphic to spec."""
    evidence = Evidence("http://example.com/evidences/1")
    evidence.related_documentation.append("https://example.com/pages/1")
    evidence.related_documentation.append("https://example.com/pages/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <http://example.com/evidences/1> a cpsv:Evidence ;
        foaf:page     <https://example.com/pages/1> ,
                      <https://example.com/pages/2> ;
    .
    """
    g1 = Graph().parse(data=evidence.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_evidence_with_languages() -> None:
    """It returns a evidence graph with dct:language isomorphic to spec."""
    evidence = Evidence("http://example.com/evidences/1")
    nob = "http://publications.europa.eu/resource/authority/language/NOB"
    eng = "http://publications.europa.eu/resource/authority/language/ENG"
    evidence.languages.append(nob)
    evidence.languages.append(eng)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/evidences/1> a cpsv:Evidence ;
        dct:language  <http://publications.europa.eu/resource/authority/language/NOB> ,
                      <http://publications.europa.eu/resource/authority/language/ENG> ;
    .
    """
    g1 = Graph().parse(data=evidence.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
