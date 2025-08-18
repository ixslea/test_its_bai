from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import VoseManager

class Quote(models.Model):
    """
    Модель цитаты

    7 свойств: текст, источник, вес, автор, дата создания (авто), кол-во просмотров, кол-во лайков
    """
    text = models.TextField(verbose_name="Текст цитаты", unique=True)
    source = models.CharField(verbose_name="Источник", default="Винкс")
    weight = models.PositiveSmallIntegerField(verbose_name="Вес цитаты",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
                                          )
    author = models.CharField(verbose_name="Ваше имя", default="ixslea")
    create_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    objects = VoseManager()

    
    @property
    def total_likes(self):
        return self.like_set.count()
    
    def user_has_liked(self, session_key):
        """
        Проверка постановки лайка пользователем по session key
        """
        if not session_key:
            return False
        return self.total_likes.filter(session_key=session_key).exists()


    @classmethod
    def increment_views_by_id(cls, quote_id):
        """
        Увеличение кол-ва просмотров на 1
        """
        quote = Quote.objects.get(id=quote_id)
        quote.views = quote.views + 1
        quote.save()
    
    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."

class Like(models.Model):
    """
    Модель лайка

    3 свойства: цитата, session key, дата создания (авто)
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='likes')
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Уникальность лайка по session_key
        """
        unique_together = ('quote', 'session_key')