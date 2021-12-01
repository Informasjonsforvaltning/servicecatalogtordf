"""Test cases for the criterion_requirement module."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import CriterionRequirement
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_criterion_requirement_with_title() -> None:
    """It returns a criterion_requirement graph with dct:title isomorphic to spec."""
    criterion_requirement = CriterionRequirement(
        "http://example.com/criterion-requirement/1"
    )
    criterion_requirement.title = {
        "en": "CriterionRequirement 1",
        "nb": "Regel 1",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .


    <http://example.com/criterion-requirement/1> a cv:CriterionRequirement ;
        dct:title   "CriterionRequirement 1"@en, "Regel 1"@nb ;
    .
    """
    g1 = Graph().parse(data=criterion_requirement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_criterion_requirement_with_dct_identifier() -> None:
    """It returns a criterion_requirement graph with dct:identifier isomorphic to spec."""
    criterion_requirement = CriterionRequirement(
        "http://example.com/criterion-requirement/1"
    )
    criterion_requirement.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/criterion-requirement/1> a cv:CriterionRequirement ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=criterion_requirement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_criterion_requirement_as_blank_node(
    mocker: MockFixture,
) -> None:
    """It returns a criterion_requirement graph with skolem uri isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    criterion_requirement = CriterionRequirement()
    criterion_requirement.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a cv:CriterionRequirement ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=criterion_requirement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_criterion_requirement_with_types() -> None:
    """It returns a criterion_requirement graph with dct:type isomorphic to spec."""
    criterion_requirement = CriterionRequirement(
        "http://example.com/criterion-requirement/1"
    )
    a_type = "http://vocabulary.com/types/1"
    another_type = "http://vocabulary.com/types/2"
    criterion_requirement.types.append(a_type)
    criterion_requirement.types.append(another_type)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/criterion-requirement/1> a cv:CriterionRequirement ;
        dct:type  <http://vocabulary.com/types/1> ,
                  <http://vocabulary.com/types/2> ;
    .
    """
    g1 = Graph().parse(data=criterion_requirement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
