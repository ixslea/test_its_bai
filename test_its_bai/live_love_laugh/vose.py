import random

class Vose:
    """
    Имплементация алгоритма Vose's Alias Method для выбора из взвешенной выборки
    """

    def __init__(self, plist):
        """
        Инициализация алгоритма 

        На вход подается список картежей (элемент, вес)
        Далее проверка на наличие элементов
        Распределение входных данных на отдельные списки элементов и их весов
        Если везде 0 вес, то равномерное распределение
        """

        if not plist:
            raise ValueError("zero elements")

        self.items = [p[0] for p in plist]
        weights = [float(p[1]) for p in plist]
        
        if not any(weights):
            weights = [1.0] * len(weights)
        
        """ 
        Инициализация таблиц Prob - вероятности и Alias - ссылки на другие элементы
        """
        self.n = len(plist)
        self.Prob = [0.0] * self.n
        self.Alias = [0] * self.n
        
        """ 
        Постороение таблиц Prob и Alias 
        """
        self._build_alias_table(weights)
    
    def _build_alias_table(self, weights):
        """
        Алгоритм построения таблиц Prob и Alias

        На вход подаются веса
        Далее их нормализация и распределение на две группы - "большие" и "маленькие" вероятности
        """

        total = sum(weights)
        scaled_weights = [w * self.n / total for w in weights]
        
        small = []
        large = []

        for i, sw in enumerate(scaled_weights):
            if sw < 1.0:
                small.append(i)
            else:
                large.append(i)
        
        while small and large:
            l = small.pop()
            g = large.pop()
            
            """ 
            Устанавливаем вероятность для элемента из "маленькой" вероятности и связаваем с элементом из "большой" 
            """
            self.Prob[l] = scaled_weights[l]
            self.Alias[l] = g
            
            """ 
            Корректируем избыток веса и возвращаем в группы 
            """
            scaled_weights[g] = (scaled_weights[g] + scaled_weights[l]) - 1.0
            
            if scaled_weights[g] < 1.0:
                small.append(g)
            else:
                large.append(g)

        """ 
        Обработка оставшихся элементов 
        """
        while large:
            g = large.pop()
            self.Prob[g] = 1.0
        
        while small:
            l = small.pop()
            self.Prob[l] = 1.0
    
    def get(self):
        """
        Генерация случайного элемента согласно заданному распределению
        Если случайное число меньше вероятности элемента возваращаем его, иначе алиас

        """
        if self.n == 0:
            return None
            
        i = random.randint(0, self.n - 1)
        if random.random() < self.Prob[i]:
            return self.items[i]
        else:
            return self.items[self.Alias[i]]