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
            username=None,
            email=None,
            phone_number=None,
            password=None,
            **extra_fields
            ):
        """
        Создает и сохраняет пользователя в зависимости от варианта регистрации
        """
        if not (email or phone_number):
            raise ParseError(
                'Поле телефон или электронная почта должно быть заполнено'
                )
        if email:
            email = self.normalize_email(email)

        if not username:
            if email:
                username = email.split('@')[0]
            else:
                username = phone_number

        user = self.model(
            username=username,
            **extra_fields
        )
        if email:
            user.email = email
        if phone_number:
            user.phone = phone_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self,
            username=None,
            email=None,
            phone_number=None,
            password=None,
            **extra_fields
            ):
        """
        Создает и сохраняет пользователя
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            phone_number=phone_number,
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

    def create_superuser(
            self,
            username=None,
            email=None,
            phone_number=None,
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
            phone_number=phone_number,
            username=username,
            email=email,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        null=True,
        blank=True,
        help_text=(
            'Введите уникальное имя пользователя. Максимум 40 символов.'
            'Используйте только английские буквы, цифры и символы @/./+/-/_'
        ),
        validators=[ASCIIUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        },
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        null=True,
        blank=True,
        help_text='Введите адрес электронной почты',
        validators=[ASCIIUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует',
        },
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        null=True,
        blank=True,
        max_length=settings.LAST_NAME_MAX_LENGTH,
        help_text='Введите фамилию'
    )

    first_name = models.CharField(
        verbose_name='Имя',
        null=True,
        blank=True,
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        help_text='Введите имя'
    )

    phone_number = models.CharField(
        max_length=settings.PHONE_MAX_LENGTH,
        blank=True,
        null=True,
        # validators=[
        #     RegexValidator(
        #         r'^(\+7|8)[0-9]{10}$',
        #         "Введите номер телефона в формате: '+79995553322'",
        #     )
        # ],
        help_text="Введите номер телефона",
    )

    date_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )

    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Картинка',
        upload_to='users/images/',
        help_text='Выберите картинку профиля',
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
        return self.get_username()
