from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from autoservice.models import Company

from users.models import CustomUser


class TestCompanyOwnerRegistration(TestCase):
    def setUp(self) -> None:
        self.test_data = {
            "email": "example@example.ru",
            "first_name": "example",
            "password": "sdr324ss92s",
            "company_name": "Cotta",
            "legal_address": "City, street, building, room",
            "inn": "231235631",
        }
        self.client = APIClient()
        self.response = self.client.post(
            "/api/v1/autoservice/companyowner/", format="json", data=self.test_data
        )

    def test_companyowner_created(self):
        users = CustomUser.objects.filter(email=self.test_data["email"])
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, self.test_data["email"])

    def test_companyowner_group_added(self):
        user: CustomUser = CustomUser.objects.get(email=self.test_data["email"])
        groups = user.groups.all()
        self.assertEqual(len(groups), 1)

    def test_company_created(self):
        company: Company = Company.objects.get(title=self.test_data["company_name"])
        self.assertEqual(company.title, self.test_data["company_name"])
        self.assertEqual(company.owner.email, self.test_data["email"])
