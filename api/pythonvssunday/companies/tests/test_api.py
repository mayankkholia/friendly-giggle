import json
import pytest
from api.pythonvssunday.companies.models import Company
from django.urls import reverse

companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db


def test_zero_companies_should_return_empty_list(client):
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succed(client):
    company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response_content.get("name") == "Amazon"
    assert response_content.get("company_status") == "HIRING_FREEZE"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_empty_arguments_should_fail(client):
    response = client.post(companies_url)
    assert response.status_code == 400


def test_create_existing_company_should_fail(client):
    company = Company.objects.create(name="Amazon")
    response = client.post(path=companies_url, data={"name": "Amazon"})
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {"name": ["company with this name already exists."]}


def test_create_company_with_layoffs_status_should_succed(client):
    response = client.post(
        path=companies_url,
        data={"name": "Amazon", "company_status": "LAYOFFS"},
    )
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content.get("company_status") == "LAYOFFS"


def test_create_company_with_wrong_status_should_succed(client):
    response = client.post(
        path=companies_url,
        data={"name": "Amazon", "company_status": "RANDOM"},
    )
    response_content = json.loads(response.content)
    assert response.status_code == 400
    # assert  response_content.get("company_status"), "LAYOFFS")


@pytest.mark.xfail
def test_flaky_test(client):
    assert 1 == 2


@pytest.mark.skip
def test_skip_test(client):
    assert 1 == 2
