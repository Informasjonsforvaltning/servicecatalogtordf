"""Test cases for the service module."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from servicecatalogtordf import (
    CriterionRequirement,
    Event,
    Evidence,
    LegalResource,
    PublicOrganization,
    Rule,
    Service,
)
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_service_with_title() -> None:
    """It returns a service graph with dct:title isomorphic to spec."""
    service = Service("http://example.com/services/1")
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


def test_to_graph_should_return_service_with_description() -> None:
    """It returns a service graph with dct:Description isomorphic to spec."""
    service = Service("http://example.com/services/1")
    service.description = {"en": "Service 1 description", "nn": "Teneste 1 skildring"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/services/1> a cpsv:PublicService ;
        dct:description   "Service 1 description"@en, "Teneste 1 skildring"@nn ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_dct_identifier() -> None:
    """It returns a service graph with dct:identifier isomorphic to spec."""
    service = Service("http://example.com/services/1")
    service.dct_identifier = "https://unique.uri.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/services/1> a cpsv:PublicService ;
        dct:identifier   "https://unique.uri.com"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_has_competent_authority() -> None:
    """It returns a service graph with cv:hasCompetentAuthority isomorphic to spec."""
    service = Service("http://example.com/services/1")
    public_organization = PublicOrganization("https://my.public.organization")
    service.has_competent_authority = public_organization

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cv:hasCompetentAuthority   <https://my.public.organization> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_follows() -> None:
    """It returns a service graph with cpsv:follows isomorphic to spec."""
    service = Service("http://example.com/services/1")
    rule = Rule("https://example.com/rules/1")
    service.follows.append(rule)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cpsv:follows   <https://example.com/rules/1> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_has_legal_resource() -> None:
    """It returns a service graph with cv:hasCompetentAuthority isomorphic to spec."""
    service = Service("http://example.com/services/1")
    legal_resource = LegalResource("https://example.com/legalresources/1")
    service.has_legal_resources.append(legal_resource)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cv:hasLegalResource   <https://example.com/legalresources/1> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_processing_time() -> None:
    """It returns a service graph with cv:processingTime isomorphic to spec."""
    service = Service("http://example.com/services/1")
    service.processing_time = "PT15M"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .


    <http://example.com/services/1> a cpsv:PublicService ;
        cv:processingTime "PT15M"^^xsd:duration ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_has_input() -> None:
    """It returns a service graph with cpsv:hasInput isomorphic to spec."""
    service = Service("http://example.com/services/1")
    evidence_1 = Evidence("http://example.com/evidences/1")
    service.has_input.append(evidence_1)
    evidence_2 = Evidence("http://example.com/evidences/2")
    service.has_input.append(evidence_2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cpsv:hasInput <http://example.com/evidences/1> ,
                      <http://example.com/evidences/2> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_is_grouped_by() -> None:
    """It returns a service graph with cv:isGroupedBy isomorphic to spec."""
    service = Service("http://example.com/services/1")
    event_1 = Event("http://example.com/events/1")
    service.is_grouped_by.append(event_1)
    event_2 = Event("http://example.com/events/2")
    service.is_grouped_by.append(event_2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cv:isGroupedBy <http://example.com/events/1> ,
                       <http://example.com/events/2> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_is_grouped_by_blank_nodes(
    mocker: MockFixture,
) -> None:
    """It returns a service graph with cv:isGroupedBy isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    service = Service("http://example.com/services/1")
    event_1 = Event()
    service.is_grouped_by.append(event_1)
    event_2 = Event()
    service.is_grouped_by.append(event_2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cv:isGroupedBy
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> ,
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_has_criterion() -> None:
    """It returns a service graph with cv:hasCriterion isomorphic to spec."""
    service = Service("http://example.com/services/1")
    criterion_requirement_1 = CriterionRequirement(
        "http://example.com/criterion-requirements/1"
    )
    service.has_criterion.append(criterion_requirement_1)
    criterion_requirement_2 = CriterionRequirement(
        "http://example.com/criterion-requirements/2"
    )
    service.has_criterion.append(criterion_requirement_2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cv:hasCriterion <http://example.com/criterion-requirements/1> ,
                        <http://example.com/criterion-requirements/2> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_service_with_has_criterion_blank_node(
    mocker: MockFixture,
) -> None:
    """It returns a service graph with cv:hasCriterion isomorphic to spec."""
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )
    service = Service("http://example.com/services/1")
    criterion_requirement_1 = CriterionRequirement()
    criterion_requirement_1.title = {"nb": "Over 20 år"}
    service.has_criterion.append(criterion_requirement_1)
    criterion_requirement_2 = CriterionRequirement()
    criterion_requirement_2.title = {"nb": "Har fast inntekt"}
    service.has_criterion.append(criterion_requirement_2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix cpsv: <http://purl.org/vocab/cpsv#> .
    @prefix cv: <http://data.europa.eu/m8g/> .

    <http://example.com/services/1> a cpsv:PublicService ;
        cv:hasCriterion
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> ,
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> ;
    .
    """
    g1 = Graph().parse(data=service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
