# Generated by Django 3.2.16 on 2023-09-19 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название работы')),
                ('description', models.CharField(max_length=150, verbose_name='Описание работы')),
                ('price', models.CharField(max_length=5, verbose_name='Относительная стоимость работ')),
                ('slug', models.CharField(max_length=150, verbose_name='Уникальный Slug')),
            ],
            options={
                'verbose_name': 'Работа',
                'verbose_name_plural': 'Работы',
                'ordering': ('name',),
            },
        ),
    ]