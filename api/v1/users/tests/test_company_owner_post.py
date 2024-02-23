from django.test import TestCase
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APIClient

from autoservice.models import Company
from users.models import CustomUser


class TestCompanyOwnerPost(TestCase):
    test_owner = {
        "email": "test_user@example.ru",
        "first_name": "test_user",
        "password": "sdr324ss92s",
        "phone_number": "+79345432643",
    }
    test_company = {
        "title": "Auto",
        "legal_address": "NewYork",
        "taxpayer_id": "0123456789",
    }
    test_company_owner = {
        "owner": test_owner,
        "company": test_company,
    }

    def setUp(self) -> None:
        self.client = APIClient()
        self.response = self.client.post(
            "/api/v1/auth/users/create-companyowner/",
            format="json",
            data=self.test_company_owner,
        )
        self.user = CustomUser.objects.get(email=self.test_owner["email"])
        self.company = Company.objects.get(title=self.test_company["title"])

    def test_post_returns_201(self):
        self.assertEqual(self.response.status_code, HTTP_201_CREATED)

    def test_post_creates_user(self):
        self.assertEqual(self.user.email, self.test_owner["email"])
        self.assertEqual(self.user.first_name, self.test_owner["first_name"])
        self.assertEqual(self.user.phone_number, self.test_owner["phone_number"])

    def test_post_adds_group_to_user(self):
        company_owners_group = self.user.groups.first().__str__()
        self.assertEqual(len(self.user.groups.all()), 1)
        self.assertEqual(company_owners_group, "company_owners")

    def test_post_creates_company(self):
        self.assertEqual(self.company.title, self.test_company["title"])
        self.assertEqual(self.company.legal_address, self.test_company["legal_address"])
        self.assertEqual(self.company.owner.email, self.test_owner["email"])
