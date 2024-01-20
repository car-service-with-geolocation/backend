from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

import api.v1.order.tests.setup_test_db as db_setup

test_user = {
    "email": "test_user@example.ru",
    "first_name": "test_user",
    "password": "sdr324ss92s",
    "phone_number": "+79345432643",
}
test_autoservice_data_path = "autoservice_short_list.json"
test_cities_data_path = "russia_city_short_list.csv"
test_user_data_path = "user_short_list.json"
test_order = {
    "car": "LADA",
    "info": "INFO",
    "task": "TASK",
    "image": "/media/autoservice/images/logo/9000RpM.jpg",
    "status": "OPENED",
    "company": "Сотта",
    "number_of_fields": 10,
}


class TestGetAllFieldsFromOrderListAPIView(TestCase):
    def setUp(self) -> None:
        db_setup.fill_db_data(test_autoservice_data_path)
        company = db_setup.get_company(test_order["company"])
        job = db_setup.get_jobs()
        autoservice = db_setup.get_autoservice_by_company(company=company)

        self.user = db_setup.get_or_create_user(test_user)

        self.order = db_setup.get_or_create_order(
            test_order,
            user=self.user,
            autoservice=autoservice,
            job=job
        )

        self.factory = APIRequestFactory()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_api_view_get_status_code_200(self):
        response = self.client.get("/api/v1/orders/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_api_view_get_all_fields(self):
        response = self.client.get("/api/v1/orders/", format="json")
        self.assertEqual(test_order["number_of_fields"], len(response.data[0]))
