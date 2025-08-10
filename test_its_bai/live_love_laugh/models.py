from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Quote(models.Model):
    text = models.TextField(verbose_name="Текст цитаты")
    author = models.CharField(verbose_name="Источник")
    weight = models.PositiveSmallIntegerField(verbose_name="Вес цитаты",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
                                          )
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."
