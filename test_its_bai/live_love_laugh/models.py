from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import VoseManager
from django.contrib.auth.models import User

class Quote(models.Model):
    text = models.TextField(verbose_name="Текст цитаты")
    source = models.CharField(verbose_name="Источник", default="Винкс")
    weight = models.PositiveSmallIntegerField(verbose_name="Вес цитаты",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
                                          )
    author = models.CharField(verbose_name="Ваше имя", default="ixslea")
    likes = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = VoseManager()

    @property
    def likes_session_keys(self):
        return list(Like.objects.filter(quote=self).values_list('session_key', flat=True))

    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."
    
class Like(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['quote', 'session_key']),
        ]