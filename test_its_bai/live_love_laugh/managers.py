from django.db import models
from django.core.cache import cache
from .vose import Vose

class VoseManager(models.Manager):
    """
    Менеджер для работы выбора цитат по Vose's Alias Method с кэширование
    """

    CACHE_KEY = 'vose_alias_data'
    
    def __init__(self):
        """
        Инициализация менеджера

        Создает пустые ссылки для объектов Vose и словаря цитат
        """
        super().__init__()
        self._vose = None
        self._quote_dict = None
    
    def _init_vose(self):
        """
        Инициализация работы взвешенного выбора

        Если есть в кэше - использует данные из кэша
        Если нет - загружает цитаты
        Запускает алгоритм Vose
        Сохраняет в кэше на час
        """
        cached_data = cache.get(self.CACHE_KEY)
        if cached_data:
            self._vose, self._quote_dict = cached_data
            return True
            
        quotes = list(self.get_queryset().values('id', 'text', 'author', 'weight', 'source', '_total_likes'))
        if not quotes:
            return False
        

        plist = [(q['id'], q['weight']) for q in quotes] 
        
        try:
            self._vose = Vose(plist)
            self._quote_dict = {q['id']: q for q in quotes}
    
            cache.set(self.CACHE_KEY, (self._vose, self._quote_dict), 3600)
            return True
        except Exception as e:
            return False
    
    def get_random(self):
        """
        Получает случайную цитату
        """
        if self._vose is None and not self._init_vose():
            return None 
        try:
            quote_id = self._vose.get()
            return self._quote_dict.get(quote_id)
        except Exception as e:
            return None
    
    def reset_cache(self):
        """
        Сбрасывает кэшированные данные
        """
        cache.delete(self.CACHE_KEY)
        self._vose = None
        self._quote_dict = None