"""Test cases for the service module."""
from rdflib import Graph

from servicecatalogtordf import Service
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_service_with_title() -> None:
    """It returns a service graph with title isomorphic to spec."""
    service = Service()
    service.identifier = "http://example.com/services/1"
    service.title = {"en": "Service 1", "nb": "Tjeneste 1"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/services/1> a cpsv:PublicService ;
        dct:title   "Service 1"@en, "Tjeneste 1"@nb ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
