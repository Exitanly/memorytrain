from django.db import models

class TaskCategory(models.Model):
    """Категории заданий"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    icon = models.CharField(max_length=50, default='bi-brain', verbose_name='Иконка')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Task(models.Model):
    """Модель задания"""
    DIFFICULTY_CHOICES = [
        (1, 'Лёгкий'),
        (2, 'Средний'),
        (3, 'Сложный'),
    ]
    
    TYPE_CHOICES = [
        ('visual', 'Визуальная память'),
        ('text', 'Текстовая память'),
        ('number', 'Числовая память'),
        ('pattern', 'Запоминание паттернов'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, verbose_name='Категория')
    task_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип задания')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1, verbose_name='Сложность')
    
    # Данные задания (в JSON формате)
    task_data = models.JSONField(verbose_name='Данные задания', default=dict)
    
    # Базовые очки за выполнение
    base_points = models.IntegerField(default=10, verbose_name='Базовые очки')
    
    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
    
    def __str__(self):
        return f"{self.title} (Ур. {self.difficulty})"
    
    def get_points(self):
        """Возвращает очки в зависимости от сложности"""
        return self.base_points * self.difficulty

class UserProgress(models.Model):
    """Прогресс пользователя по заданиям"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задание')
    completed = models.BooleanField(default=False, verbose_name='Выполнено')
    score = models.IntegerField(default=0, verbose_name='Набранные очки')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата выполнения')
    attempts = models.IntegerField(default=1, verbose_name='Попытки')
    
    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
        unique_together = ['user', 'task']  # Пользователь не может выполнить задание дважды
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title}"