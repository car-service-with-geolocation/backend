from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_all_isdigit(value: str) -> None:
    if not all((char.isdigit() for char in value)):
        raise ValidationError(
            _("%(value) contains not digit characters"),
            params={"value": value},
        )
