![Tests](https://github.com/Informasjonsforvaltning/servicecatalogtordf/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/servicecatalogtordf/branch/main/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/servicecatalogtordf)
[![PyPI](https://img.shields.io/pypi/v/servicecatalogtordf.svg)](https://pypi.org/project/servicecatalogtordf/)
[![Read the Docs](https://readthedocs.org/projects/servicecatalogtordf/badge/)](https://servicecatalogtordf.readthedocs.io/)
# servicecatalogtordf
A library that will map a service catalog (cpsv) to rdf

The library contains helper classes for the following cpsv and related classes:
 - [PublicService](https://data.norge.no/specification/dcat-ap-no/#klasse-offentlig-tjeneste)
 - [PublicOrganization](https://data.norge.no/specification/dcat-ap-no/#klasse-offentlig-organisasjon)
 - [LegalResource](https://data.norge.no/specification/dcat-ap-no/#klasse-regulativ-ressurs)
 - [Rule](https://data.norge.no/specification/dcat-ap-no/#klasse-regel)
 - [Evidence](https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/core-public-service-vocabulary-application-profile)
 - [Event](https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/core-public-service-vocabulary-application-profile)


## Usage
### Install
```
% pip install servicecatalogtordf
```
### Getting started
```
from datacatalogtordf import Catalog
from servicecatalogtordf import PublicOrganization, Service

# Create catalog object
catalog = Catalog()
catalog.identifier = "http://example.com/catalogs/1"
catalog.title = {"en": "A service catalog"}
catalog.publisher = "https://example.com/publishers/1"

# Create a service:
service = Service("http://example.com/services/1")
service.title = {"nb": "inntektsAPI", "en": "incomeAPI"}
# Create a public organization:
public_organization = PublicOrganization("https://example.com/publishers/1")
# Add it to the service:
service.has_competent_authority = public_organization
#
# Add service to catalog:
catalog.services.append(service)

# Get rdf representation in turtle (default)
rdf = catalog.to_rdf()
print(rdf)
```
## Development
### Requirements
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [pipx](https://github.com/pipxproject/pipx) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://github.com/cjolowicz/nox-poetry)

```
% pipx install poetry==1.1.7
% pipx install nox==2021.06.12
% pipx inject nox nox-poetry
```
### Install
```
% git clone https://github.com/Informasjonsforvaltning/servicecatalogtordf.git
% cd servicecatalogtordf
% pyenv install 3.7.11
% pyenv install 3.8.11
% pyenv install 3.9.6
% pyenv local 3.7.11 3.8.11 3.9.6
% poetry install
```
### Run all sessions
```
% nox
```
### Run all tests with coverage reporting
```
% nox -rs tests
```
### Debugging
You can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:
```
nox -rs tests -- --pdb
```
You can set breakpoints directly in code by using the function `breakpoint()`.
