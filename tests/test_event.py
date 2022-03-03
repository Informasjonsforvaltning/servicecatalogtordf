"""Test cases for the event module."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import Event
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_event_as_blank_node(
    mocker: MockFixture,
) -> None:
    """It returns a event graph with skolem uri isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    event = Event()
    event.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a cpsv:Event ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=event.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_event_with_dct_identifier() -> None:
    """It returns a event graph with dct:identifier isomorphic to spec."""
    event = Event("http://example.com/events/1")
    event.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/events/1> a cpsv:Event ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=event.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_event_with_name() -> None:
    """It returns a event graph with dct:title isomorphic to spec."""
    event = Event("http://example.com/events/1")
    event.name = {
        "en": "Event 1",
        "nb": "Bevis 1",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/events/1> a cpsv:Event ;
        dct:title  "Event 1"@en ,
                  "Bevis 1"@nb ;
    .
    """
    g1 = Graph().parse(data=event.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_event_with_description() -> None:
    """It returns a event graph with dct:description isomorphic to spec."""
    event = Event("http://example.com/events/1")
    event.description = {
        "en": "Event 1 description",
        "nb": "Bevis 1 beskrivelse",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/events/1> a cpsv:Event ;
        dct:description  "Event 1 description"@en ,
                         "Bevis 1 beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=event.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_event_with_type() -> None:
    """It returns a event graph with dct:type isomorphic to spec."""
    event = Event("http://example.com/events/1")
    event.type = "http://example.com/concepts/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/events/1> a cpsv:Event ;
        dct:type  <http://example.com/concepts/1> ;
    .
    """
    g1 = Graph().parse(data=event.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_event_with_related_service() -> None:
    """It returns a event graph with dct:relation isomorphic to spec."""
    event = Event("http://example.com/events/1")
    event.related_service.append("https://example.com/services/1")
    event.related_service.append("https://example.com/services/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/events/1> a cpsv:Event ;
        dct:relation   <https://example.com/services/1> ,
                       <https://example.com/services/2> ;
    .
    """
    g1 = Graph().parse(data=event.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
