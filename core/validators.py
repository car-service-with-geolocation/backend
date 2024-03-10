from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def validate_all_isdigit(value: str) -> None:
    if not all((char.isdigit() for char in value)):
        raise ValidationError(
            _("%(value) contains not digit characters"),
            params={"value": value},
        )


phone_number_validator = RegexValidator(
    r"^(\+7|8)[0-9]{10}$",
    "Введите номер телефона в формате: '+79995553322'",
)
