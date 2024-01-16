from django.test import TestCase

from api.v1.users.serializers import CustomCurrentUserSerializer
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
        )
        self.user = CustomUser.objects.get(email=test_user["email"])
        self.serializer = CustomCurrentUserSerializer(partial=True)

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
