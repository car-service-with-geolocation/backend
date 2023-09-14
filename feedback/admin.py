from django.contrib import admin
from django.contrib.admin import register

from models import Feedback


@register(Feedback)
class FeedbackAdmin:
    """
    Кастомизация модели Feedback в админ панеле.
    """
    list_display = ('author', 'text', 'pub_date', 'auto_service', 'score')
    list_filter = ('auto_service', 'pub_date')
    save_on_top = True
