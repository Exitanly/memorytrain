import random
import time
from abc import ABC, abstractmethod

class BaseTaskGenerator(ABC):
    """Базовый класс для всех генераторов заданий"""
    
    def __init__(self, difficulty=1):
        """
        difficulty: 1 - лёгкий, 2 - средний, 3 - сложный
        """
        self.difficulty = difficulty
        self.task_data = None
        self.start_time = None
    
    @abstractmethod
    def generate(self):
        """
        Генерирует задание.
        Возвращает словарь с данными для шаблона:
        {
            'task_data': {...},  # Данные для отображения
            'check_data': {...}, # Данные для проверки (сохраняются в сессии)
            'max_time': int,     # Максимальное время в секундах
        }
        """
        pass
    
    @abstractmethod
    def check_answer(self, user_answer, check_data):
        """
        Проверяет ответ пользователя.
        Возвращает: (is_correct, message)
        """
        pass
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        """Расчёт очков с учётом времени и попыток"""
        if not is_correct:
            return 0
        
        base_points = {1: 10, 2: 15, 3: 20}[self.difficulty]
        
        # Максимальное время для этого задания (по умолчанию 30 сек)
        max_time = getattr(self, 'max_time', 30)
        
        # Бонус за скорость (до +50%)
        time_bonus = max(0, (1 - min(time_spent, max_time) / max_time)) * 0.5
        
        # Штраф за попытки (первая попытка без штрафа)
        attempt_penalty = (attempts - 1) * 0.1
        
        multiplier = 1 + time_bonus - attempt_penalty
        multiplier = max(0.5, min(1.5, multiplier))
        
        return round(base_points * multiplier)
    
    def start_timer(self):
        """Запуск таймера"""
        self.start_time = time.time()
    
    def get_time_spent(self):
        """Получить затраченное время"""
        if self.start_time:
            return time.time() - self.start_time
        return 0