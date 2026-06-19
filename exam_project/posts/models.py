# employees/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Posts(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок поста"
    )
    content = models.TextField(
        verbose_name="Содержание поста"
    )
    published_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    views = models.IntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )
    is_published = models.BooleanField(
        default=False, verbose_name="Опубликован/черновик"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания записи"
    )

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if not self.title or self.title.strip() == '':
            raise ValidationError({'title': 'Заголовок не может быть пустым.'})
        
        if not self.content or self.content.strip() == '':
            raise ValidationError({'content': 'Содержание не может быть пустым.'})
        
        if self.published_at and self.published_at > timezone.now().date():
            raise ValidationError({'published_at': 'Дата публикации не может быть в будущем.'})
        
        if self.views is not None and self.views < 0:
            raise ValidationError({'views': 'Просмотры не могут быть меньше 0.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)