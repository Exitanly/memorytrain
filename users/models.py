from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Расширенная модель пользователя"""
    level = models.IntegerField(default=1, verbose_name='Уровень')
    experience = models.IntegerField(default=0, verbose_name='Опыт')
    total_points = models.IntegerField(default=0, verbose_name='Всего очков')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
    
    def get_exp_for_next_level(self):
        """Возвращает количество опыта, необходимого для достижения следующего уровня"""
        if self.level < 5:
            return 50
        elif self.level < 10:
            return 120
        else:
            return 150
    
    def get_exp_needed_for_level(self, target_level):
        """Возвращает суммарный опыт, необходимый для достижения target_level"""
        if target_level <= 1:
            return 0
        
        exp = 0
        for level in range(2, target_level + 1):
            if level < 5:
                exp += 50
            elif level < 10:
                exp += 120
            else:
                exp += 150
        return exp
    
    def get_exp_progress(self):
        """Возвращает прогресс до следующего уровня (в процентах)"""
        if self.level == 1:
            exp_for_current = 0
        else:
            exp_for_current = self.get_exp_needed_for_level(self.level)
        
        exp_for_next = self.get_exp_needed_for_level(self.level + 1)
        exp_earned_in_current = self.experience - exp_for_current
        
        needed = exp_for_next - exp_for_current
        
        if needed <= 0:
            return 100
        
        percent = (exp_earned_in_current / needed) * 100
        return min(100, max(0, percent))
    
    def get_exp_current_display(self):
        """Отображает текущий опыт в формате '50/100'"""
        if self.level == 1:
            exp_for_current = 0
        else:
            exp_for_current = self.get_exp_needed_for_level(self.level)
        
        exp_for_next = self.get_exp_needed_for_level(self.level + 1)
        current = self.experience - exp_for_current
        needed = exp_for_next - exp_for_current
        
        return f"{current}/{needed}"
    
    def add_experience(self, points):
        """Добавление опыта и повышение уровня"""
        self.experience += points
        self.total_points += points
        
        level_up = False
        
        # Проверяем, нужно ли повысить уровень
        while True:
            exp_needed_for_next = self.get_exp_needed_for_level(self.level + 1)
            if self.experience >= exp_needed_for_next:
                self.level += 1
                level_up = True
            else:
                break
        
        self.save()
        return level_up
    
    
    def can_access_difficulty(self, difficulty):
    
        if difficulty == 1:
            return True
        elif difficulty == 2:
            return self.level >= 5
        elif difficulty == 3:
            return self.level >= 10
        return False