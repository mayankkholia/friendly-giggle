import json
from unittest import TestCase

import pytest
from api.pythonvssunday.companies.models import Company
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class BaseCompanyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self):
        pass


class TestGetCompanies(BaseCompanyTestCase):

    def test_zero_companies_should_return_empty_list(self):
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succed(self):
        company = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response_content.get("name"), "Amazon")
        self.assertEqual(response_content.get("company_status"), "HIRING_FREEZE")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")


class TestPostCompanies(BaseCompanyTestCase):
    def test_create_company_with_empty_arguments_should_fail(self):
        response = self.client.post(self.companies_url)
        self.assertEqual(response.status_code, 400)

    def test_create_existing_company_should_fail(self):
        company = Company.objects.create(name="Amazon")
        response = self.client.post(path=self.companies_url, data={"name": "Amazon"})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_content, {"name": ["company with this name already exists."]}
        )

    def test_create_company_with_layoffs_status_should_succed(self):
        response = self.client.post(
            path=self.companies_url,
            data={"name": "Amazon", "company_status": "LAYOFFS"},
        )
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get("company_status"), "LAYOFFS")

    def test_create_company_with_wrong_status_should_succed(self):
        response = self.client.post(
            path=self.companies_url,
            data={"name": "Amazon", "company_status": "RANDOM"},
        )
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response_content.get("company_status"), "LAYOFFS")

    @pytest.mark.xfail
    def test_flaky_test(self):
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_skip_test(self):
        self.assertEqual(1, 2)
