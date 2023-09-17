from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from autoservice.models import AutoService

User = get_user_model()


class Feedback(models.Model):
    '''Отзывы на АвтоСервисы от пользователя.'''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )
    autoservice = models.ForeignKey(
        AutoService,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Автосервис'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, message='Оценка ниже 1 невозможна'),
                    MaxValueValidator(5, message='Оценка выше 5 невозможна')],
        verbose_name='Оценка автосервиса от пользователя'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'autoservice'], name='unique_feedback'
            )
        ]

    def __str__(self) -> str:
        return f'{self.author.get_username}: {self.text[:25]}'
