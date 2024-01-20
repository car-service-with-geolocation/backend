import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from api.v1.users.serializers import CustomCurrentUserSerializer
from api.v1.users.views import CustomUserViewSet
from users.models import CustomUser

test_user = {
    "email": "test_user@example.ru",
    "first_name": "test_user",
    "password": "sdr324ss92s",
    "phone_number": "+79345432643",
}


class TestCurrentUserPatch(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create(
            email=test_user["email"],
            first_name=test_user["first_name"],
            password=test_user["password"],
            phone_number=test_user["phone_number"],
        )
        self.user = CustomUser.objects.get(email=test_user["email"])
        self.serializer = CustomCurrentUserSerializer(partial=True)
        self.factory = APIRequestFactory()

    def test_serializer_update_without_password(self) -> None:
        patch_data = {"email": "test_user@example.ru", "phone_number": "+79111111111"}
        user: CustomUser = self.serializer.update(self.user, patch_data)
        self.assertEqual(user.phone_number, patch_data["phone_number"])
        self.assertEqual(user.email, patch_data["email"])

        user_from_db = CustomUser.objects.get(email=test_user["email"])
        self.assertEqual(user_from_db.phone_number, patch_data["phone_number"])

    def test_serializer_update_with_password(self) -> None:
        patch_data = {
            "email": "test_user@example.ru",
            "phone_number": "+79111111111",
            "password": test_user["password"],
        }
        user: CustomUser = self.serializer.update(self.user, patch_data)
        self.assertEqual(user.phone_number, patch_data["phone_number"])
        self.assertEqual(user.email, patch_data["email"])

        user_from_db = CustomUser.objects.get(email=test_user["email"])
        self.assertEqual(user_from_db.phone_number, patch_data["phone_number"])

    def test_class_view_with_patch_request(self):
        test_data = [
            {
                "email": test_user["email"],
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": test_user["password"],
            },
            {
                "email": test_user["email"],
                "first_name": "changed",
                "phone_number": "+79111111112",
            },
            {
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": test_user["password"],
            },
            {
                "email": "second_example@example.com",
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": test_user["password"],
            },
            {
                "email": test_user["email"],
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": "dsa92-hap",
            },
            {
                "email": "second_example@example.com",
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": "dsa92-hap",
            },
        ]
        for patch in test_data:
            with self.subTest(msg=patch):
                request = self.factory.patch(
                    "/api/v1/auth/users/me/",
                    json.dumps(patch),
                    content_type="application/json",
                )
                force_authenticate(request, user=self.user)
                view = CustomUserViewSet.as_view({"patch": "me"})
                response = view(request)
                self.assertEqual(response.status_code, 200)


    def test_class_view_with_put_request(self):
        test_data = [
            {
                "email": test_user["email"],
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": test_user["password"],
            },
            {
                "email": "second_example@example.com",
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": test_user["password"],
            },
            {
                "email": test_user["email"],
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": "dsa92-hap",
            },
            {
                "email": "second_example@example.com",
                "first_name": "changed",
                "phone_number": "+79111111112",
                "password": "dsa92-hap",
            },
        ]
        for put in test_data:
            with self.subTest(msg=put):
                request = self.factory.put(
                    "/api/v1/auth/users/me/",
                    json.dumps(put),
                    content_type="application/json",
                )
                force_authenticate(request, user=self.user)
                view = CustomUserViewSet.as_view({"put": "me"})
                response = view(request)
                self.assertEqual(response.status_code, 200)
