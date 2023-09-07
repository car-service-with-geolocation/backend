from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
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
        help_text='Введите адрес электронной почты',
        validators=[ASCIIUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует',
        },
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LAST_NAME_MAX_LENGTH,
        help_text='Введите фамилию'
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        help_text='Введите имя'
    )

    phone = models.CharField(
        verbose_name='Номер телефона',
        help_text='Введите номер телефона',
        validators=[
            validators.RegexValidator(
                r'^+[0-9]{11}$',
                'Используйте цифры от 0 до 9, начинайте ввод с +7',
            )
        ],
    )
    date_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='users/images/',
        help_text='Выберите картинку профиля',
    )
    is_staff = models.BooleanField(
        verbose_name='Статус сотрудника',
        default=False
    )
    is_verified = models.BooleanField(
        verbose_name='Верификация профиля',
        default=False
    )

    # order = ForeignKey(Order)
    # favorite = ManyToMany(Service)
    # comment = ManyToMany(Comment)

    class Meta:
        ordering = ('email', )
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_username()
