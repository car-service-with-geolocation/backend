from django.contrib.auth.models import Group
from django.db.models import QuerySet

from autoservice.models import AutoService, Company, Job
from core.management.commands.import_autoservice import (
    Command as CreateAutoserviciesCommand,
)
from core.management.commands.import_city import Command as CreateCitiesCommand
from core.management.commands.import_user import Command as CreateUsersCommand
from order.models import Order
from users.models import CustomUser

test_autoservice_data_path = "autoservice_short_list.json"
test_cities_data_path = "russia_city_short_list.csv"
test_user_data_path = "user_short_list.json"


def fill_db_data(
    autoservice_file_path=test_autoservice_data_path,
    cities_file_path=test_cities_data_path,
    user_file_path=test_user_data_path,
):
    CreateCitiesCommand().handle(cities_file_path)
    CreateAutoserviciesCommand().handle(autoservice_file_path)
    CreateUsersCommand().handle(user_file_path)


def get_jobs(title: str = "предрейсовый техосмотр") -> QuerySet[Job]:
    return Job.objects.filter(title=title)


def get_company(title: str):
    return Company.objects.get(title=title)


def get_or_create_company(company_data: dict):
    company, _ = Company.objects.get_or_create(**company_data)
    return company


def get_autoservice_by_company(company: Company):
    return AutoService.objects.get(company=company)


def get_or_create_user(user_data: dict):
    user, _ = CustomUser.objects.get_or_create(**user_data)
    return user


def add_user_to_group(user: CustomUser, group_name: str):
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    user.save()


def get_or_create_order(order_data: dict, user, autoservice, job):
    order, _ = Order.objects.get_or_create(
        car=order_data["car"],
        info=order_data["info"],
        task=order_data["task"],
        status=order_data["status"],
        owner=user,
        autoservice=autoservice,
    )
    order.jobs.set(job)
    return order
