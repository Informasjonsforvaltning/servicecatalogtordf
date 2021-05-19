"""Test cases for the public_organization module."""
from datacatalogtordf import Location
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import PublicOrganization
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_public_organization_with_title() -> None:
    """It returns a public_organization graph with dct:title isomorphic to spec."""
    public_organization = PublicOrganization(
        "http://example.com/public-organizations/1"
    )
    public_organization.title = {
        "en": "PublicOrganization 1",
        "nb": "Offentlig organisasjon 1",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/public-organizations/1> a cv:PublicOrganization ;
        dct:title   "PublicOrganization 1"@en, "Offentlig organisasjon 1"@nb ;
    .
    """
    g1 = Graph().parse(data=public_organization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_public_organization_with_dct_identifier() -> None:
    """It returns a public_organization graph with dct:identifier isomorphic to spec."""
    public_organization = PublicOrganization(
        "http://example.com/public-organizations/1"
    )
    public_organization.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/public-organizations/1> a cv:PublicOrganization ;
        dct:identifier   "https://unique.uri.com" ;
    .
    """
    g1 = Graph().parse(data=public_organization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_public_organization_as_blank_node(
    mocker: MockFixture,
) -> None:
    """It returns a public_organization graph with skolem uri isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    public_organization = PublicOrganization()
    public_organization.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a cv:PublicOrganization ;
        dct:identifier   "https://unique.uri.com" ;
    .
    """
    g1 = Graph().parse(data=public_organization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_public_organization_with_pref_label() -> None:
    """It returns a public_organization graph with skos:prefLabel isomorphic to spec."""
    public_organization = PublicOrganization(
        "http://example.com/public-organizations/1"
    )
    public_organization.pref_label = {
        "en": "PublicOrganization 1 prefLabel",
        "nb": "Offentlig organisasjon 1 prefLabel",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/public-organizations/1> a cv:PublicOrganization ;
        skos:prefLabel   "PublicOrganization 1 prefLabel"@en ,
                         "Offentlig organisasjon 1 prefLabel"@nb ;
    .
    """
    g1 = Graph().parse(data=public_organization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_public_organization_with_spatial_coverage() -> None:
    """It returns a public_organization graph with dct:spatial isomorphic to spec."""
    public_organization = PublicOrganization(
        "http://example.com/public-organizations/1"
    )
    location = Location()
    location.identifier = "http://publications.europa.eu/resource/authority/country/NOR"
    public_organization.spatial_coverage = location

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/public-organizations/1> a cv:PublicOrganization ;
        dct:spatial <http://publications.europa.eu/resource/authority/country/NOR> ;
    .
    """
    g1 = Graph().parse(data=public_organization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
