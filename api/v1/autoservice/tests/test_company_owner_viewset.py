from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.v1.order.tests.setup_test_db import (
    add_user_to_group,
    get_or_create_company,
    get_or_create_user,
)

test_user = {
    "email": "test_user@example.ru",
    "first_name": "test_user",
    "password": "sdr324ss92s",
    "phone_number": "+79345432643",
}
test_company = {
    "title": "Sotta",
    "description": "The Best",
    "legal_address": "Moscow, Red Square",
    "taxpayer_id": "0123456789",
}
group_name = "company_owners"


def setup_initial_state_and_return_user(user, company, group):
    user_instance = get_or_create_user(user)
    add_user_to_group(user_instance, group)
    company_instance = get_or_create_company(company)
    company_instance.owner = user_instance
    company_instance.save()
    return user_instance


class TestCompanyOwnerGet(TestCase):
    def setUp(self) -> None:
        user = setup_initial_state_and_return_user(test_user, test_company, group_name)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.response = self.client.get("/api/v1/autoservice/me/", format="json")

    def test_get_status_code_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_response_data(self) -> None:
        self.assertEqual(self.response.data["taxpayer_id"], test_company["taxpayer_id"])
        self.assertEqual(self.response.data["company"], 1)
