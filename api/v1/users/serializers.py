from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from users.models import CustomUser


class CustomUserSerializer(UserSerializer):
    image = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('id',
                  'email',
                  'username',
                  'telegram_id',
                  'phone',
                  'first_name',
                  'last_name',
                  'date_joined'
                  )

