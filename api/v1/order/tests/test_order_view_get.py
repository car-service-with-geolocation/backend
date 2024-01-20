from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from autoservice.models import AutoService, Company, Job
from core.management.commands.import_autoservice import (
    Command as CreateAutoserviciesCommand,
)
from core.management.commands.import_city import Command as CreateCitiesCommand
from order.models import Order
from users.models import CustomUser

test_user = {
    "email": "test_user@example.ru",
    "first_name": "test_user",
    "password": "sdr324ss92s",
    "phone_number": "+79345432643",
}
test_autoservice_data_path = "autoservice_short_list.json"
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
        CreateCitiesCommand().handle()
        CreateAutoserviciesCommand().handle(test_autoservice_data_path)

        job = Job.objects.filter(title="предрейсовый техосмотр")
        company = Company.objects.get(title=test_order["company"])
        autoservice = AutoService.objects.get(company=company)

        self.user, _ = CustomUser.objects.get_or_create(
            email=test_user["email"],
            first_name=test_user["first_name"],
            password=test_user["password"],
        )

        self.order, _ = Order.objects.get_or_create(
            owner=self.user,
            car=test_order["car"],
            info=test_order["info"],
            task=test_order["task"],
            image=test_order["image"],
            status=test_order["status"],
            autoservice=autoservice,
        )
        self.order.jobs.set(job)

        self.factory = APIRequestFactory()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_api_view_get_status_code_200(self):
        response = self.client.get("/api/v1/orders/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_api_view_get_all_fields(self):
        response = self.client.get("/api/v1/orders/", format="json")
        self.assertEqual(test_order["number_of_fields"], len(response.data[0]))
