# Generated by Django 3.2.16 on 2023-09-19 19:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0002_auto_20230919_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autoservicejob',
            options={'verbose_name': 'работу', 'verbose_name_plural': 'Работы и прайсы автосервисов'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Город', 'verbose_name_plural': 'Города РФ'},
        ),
        migrations.AlterModelOptions(
            name='geolocationautoservice',
            options={'verbose_name': 'геолокацию', 'verbose_name_plural': 'Геолокация автосервисов РФ'},
        ),
        migrations.AlterModelOptions(
            name='geolocationcity',
            options={'verbose_name': 'геолокацию', 'verbose_name_plural': 'Геолокация городов РФ'},
        ),
        migrations.AlterField(
            model_name='autoservice',
            name='phone_number',
            field=models.CharField(help_text='Введите номер телефона в формате +79995553322', max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,12}$', message="Ошибка ввода, используйте формат: '+79995553322'")], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='autoservice',
            name='rating',
            field=models.PositiveSmallIntegerField(help_text='Укажите рейтинг автосервиса', validators=[django.core.validators.MinValueValidator(1, message='Оценка ниже 1 невозможна'), django.core.validators.MaxValueValidator(10, message='Оценка выше 10 невозможна')], verbose_name='Рейтинг автосервиса'),
        ),
        migrations.AlterField(
            model_name='autoservicejob',
            name='price',
            field=models.CharField(max_length=5, validators=[django.core.validators.MinValueValidator(1, message='Стоимость ниже 1 невозможна')], verbose_name='Относительная стоимость работ'),
        ),
    ]