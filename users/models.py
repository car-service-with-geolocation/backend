from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self,
            email=None,
            first_name=None,
            password=None,
            **extra_fields
            ):
        """
        Создает и сохраняет пользователя в зависимости от варианта регистрации
        """
        if not email:
            raise ParseError(
                'Поле электронная почта должно быть заполнено'
                )
        if not first_name:
            raise ParseError(
                'Поле Имя должно быть заполнено'
            )

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self,
            email=None,
            first_name=None,
            password=None,
            **extra_fields
            ):
        """
        Создает и сохраняет пользователя
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            first_name=first_name,
            password=password,
            **extra_fields
        )

    def create_superuser(
            self,
            email=None,
            first_name=None,
            password=None,
            **extra_fields
            ):
        """
        Создает и сохраняет супер-пользователя
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email=email,
            first_name=first_name,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        null=False,
        help_text='Введите адрес электронной почты',
        validators=[ASCIIUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует',
        },
    )

    first_name = models.CharField(
        verbose_name='Имя',
        null=False,
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        help_text='Введите имя'
    )

    phone_number = models.CharField(
        max_length=settings.PHONE_MAX_LENGTH,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                r'^(\+7|8)[0-9]{10}$',
                "Введите номер телефона в формате: '+79995553322'",
            )
        ],
        help_text="Введите номер телефона",
    )

    date_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )

    is_staff = models.BooleanField(
        verbose_name='Категория пользователя',
        default=False
    )
    is_verified = models.BooleanField(
        verbose_name='Верификация профиля',
        default=False
    )

    is_active = models.BooleanField(
        verbose_name='Статус пользователя',
        default=False
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ('email', )
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.email)
