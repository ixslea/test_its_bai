from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .managers import VoseManager
from django.contrib.auth.models import User

class Quote(models.Model):
    text = models.TextField(verbose_name="Текст цитаты", unique=True)
    source = models.CharField(verbose_name="Источник", default="Винкс")
    weight = models.PositiveSmallIntegerField(verbose_name="Вес цитаты",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
                                          )
    author = models.CharField(verbose_name="Ваше имя", default="ixslea")
    likes = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    objects = VoseManager()

    @property
    def total_likes(self):
        return self.like_set.count()
    
    def user_has_liked(self, session_key):
        if not session_key:
            return False
        return self.like_set.filter(session_key=session_key).exists()


    @classmethod
    def increment_views_by_id(cls, quote_id):
        quote = Quote.objects.get(id=quote_id)
        quote.views = quote.views + 1
        quote.save()
    
   

    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."

class Like(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quote', 'session_key')