import io

from django.test import TestCase
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

import api.v1.order.tests.setup_test_db as db_setup
from order.models import OrderImages

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
    "phone_number": "+79633114455",
    "number_of_fields": 9,
}

another_user = {
    "email": "another_user@example.ru",
    "first_name": "another_user",
    "password": "safadh3kla",
    "phone_number": "+79842422643",
}


def generate_image_file():
    file = io.BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file


class TestGetAllFieldsFromOrderListAPIView(TestCase):
    def setUp(self) -> None:
        db_setup.fill_db_data(test_autoservice_data_path)
        company = db_setup.get_company(test_order["company"])
        job = db_setup.get_jobs()
        autoservice = db_setup.get_autoservice_by_company(company=company)

        self.user = db_setup.get_or_create_user(test_user)

        self.order = db_setup.get_or_create_order(
            test_order, user=self.user, autoservice=autoservice, job=job
        )

        self.another_user = db_setup.get_or_create_user(another_user)
        db_setup.get_or_create_order(
            test_order, user=self.another_user, autoservice=autoservice, job=job
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_current_user_list_api_view_get_status_code_200(self):
        response = self.client.get("/api/v1/orders/me/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_user_list_api_view_get_all_fields(self):
        number_of_current_user_orders = 1
        response = self.client.get("/api/v1/orders/me/", format="json")
        self.assertEqual(number_of_current_user_orders, len(response.data))


class TestPostCurrentUserOrderListAPIView(TestCase):
    def setUp(self) -> None:
        db_setup.fill_db_data(test_autoservice_data_path)
        company = db_setup.get_company(test_order["company"])
        job = db_setup.get_jobs()
        autoservice = db_setup.get_autoservice_by_company(company=company)

        self.user = db_setup.get_or_create_user(test_user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.post_order = [
            {
                "car": "LADA",
                "info": "INFO",
                "task": "TASK",
                "status": "OPENED",
                "jobs": [job[0].id],
                "autoservice": autoservice.id,
                "phone_number": "+79633114455",
            },
            {
                "car": "LADA",
                "info": "INFO",
                "task": "TASK",
                "status": "OPENED",
                "autoservice": autoservice.id,
            },
            {
                "car": "LADA",
                "info": "INFO",
                "task": "TASK",
                "jobs": [job[0].id],
                "autoservice": autoservice.id,
                "phone_number": "+79633114455",
            },
            {
                "car": "LADA",
                "task": "TASK",
                "status": "OPENED",
                "jobs": [job[0].id],
                "autoservice": autoservice.id,
                "phone_number": "+79633114455",
            },
            {
                "car": "LADA",
                "info": "INFO",
                "status": "OPENED",
                "jobs": [job[0].id],
                "autoservice": autoservice.id,
                "phone_number": "+79633114455",
            },
        ]

    def test_current_user_list_api_view_get_status_code_200(self):
        for post in self.post_order:
            with self.subTest(msg=post):
                response = self.client.post(
                    "/api/v1/orders/me/", format="json", data=post
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
