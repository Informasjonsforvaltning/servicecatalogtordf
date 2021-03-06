Service catalog to RDF library
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

A small Python library for mapping a service catalog to rdf

`Link text <link URL>`_

The library contains helper classes for the following cpsv and related classes:
- `PublicService <https://data.norge.no/specification/dcat-ap-no/#klasse-offentlig-tjeneste>`_
- `PublicOrganization <https://data.norge.no/specification/dcat-ap-no/#klasse-offentlig-organisasjon>`_
- `LegalResource <https://data.norge.no/specification/dcat-ap-no/#klasse-regulativ-ressurs>`_
- `Rule <https://data.norge.no/specification/dcat-ap-no/#klasse-regel>`_
- `Evidence <https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/core-public-service-vocabulary-application-profile>`_
- `Event <https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/core-public-service-vocabulary-application-profile>`_
`

The library will map to `the Norwegian Application Profile <https://data.norge.no/specification/dcat-ap-no/>`_ of `the DCAT standard <https://www.w3.org/TR/vocab-dcat-2/>`_.

Installation
------------

To install the servicecatalogtordf package,
run this command in your terminal:

.. code-block:: console

   $ pip install servicecatalogtordf


Usage
-----

This package can be used like this:

.. code-block::

  from datacatalogtordf import Catalog
  from servicecatalogtordf import PublicOrganization, Service

  # Create catalog object
  catalog = Catalog()
  catalog.identifier = "http://example.com/catalogs/1"
  catalog.title = {"en": "A service catalog"}
  catalog.publisher = "https://example.com/publishers/1"

  # Create a service:
  service = Service()
  service.identifier = "http://example.com/services/1"
  service.title = {"nb": "inntektsAPI", "en": "incomeAPI"}
  #
  # Create a public organization:
  public_organization = PublicOrganization("https://example.com/publishers/1")
  # Add it to the service:
  service.has_competent_authority = public_organization
  #
  # Add service to catalog:
  catalog.contains_services.append(service)

  # Get rdf representation in turtle (default)
  rdf = catalog.to_rdf()
  print(rdf)
