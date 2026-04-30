from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Дополнительные поля для нашего приложения
    level = models.IntegerField(default=1, verbose_name='Уровень')
    experience = models.IntegerField(default=0, verbose_name='Опыт')
    total_points = models.IntegerField(default=0, verbose_name='Всего очков')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
    
    def add_experience(self, points):
        """Добавление опыта и повышение уровня"""
        self.experience += points
        self.total_points += points
        
        # Формула уровня: нужно exp = 100 * уровень
        required_exp = self.level * 100
        if self.experience >= required_exp:
            self.level += 1
            self.experience = self.experience - required_exp
            return True  # Уровень повышен
        return False  # Уровень не повышен