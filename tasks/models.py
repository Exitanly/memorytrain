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
    """Модель задания (старая, для обратной совместимости)"""
    
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
    """Прогресс пользователя по заданиям (старый)"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задание')
    completed = models.BooleanField(default=False, verbose_name='Выполнено')
    score = models.IntegerField(default=0, verbose_name='Набранные очки')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата выполнения')
    attempts = models.IntegerField(default=1, verbose_name='Попытки')
    
    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
        unique_together = ['user', 'task']
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title}"


# ========== НОВАЯ АРХИТЕКТУРА ==========

class ExerciseType(models.Model):
    """Тип упражнения (например, 'Карточки', 'Слепое действие')"""
    
    CATEGORY_CHOICES = [
        ('visual', 'Визуальная память'),
        ('number', 'Числовая память'),
        ('text', 'Текстовая память'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL-идентификатор')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    instruction = models.TextField(verbose_name='Инструкция для пользователя')
    icon = models.CharField(max_length=50, default='bi-puzzle', verbose_name='Иконка')
    
    # Класс-генератор (будет вызван по имени)
    generator_class = models.CharField(max_length=100, verbose_name='Класс генератора')
    
    # Настройки
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    
    class Meta:
        verbose_name = 'Тип упражнения'
        verbose_name_plural = 'Типы упражнений'
        ordering = ['category', 'order']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"


class ExerciseSession(models.Model):
    """Сессия выполнения упражнения (сохраняет только результат, не само задание)"""
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE, verbose_name='Тип упражнения')
    
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Начало')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершение')
    
    score = models.IntegerField(default=0, verbose_name='Начисленные очки')
    is_completed = models.BooleanField(default=False, verbose_name='Завершено')
    
    # Детали выполнения (попытки, время, уровень сложности)
    details = models.JSONField(default=dict, verbose_name='Детали')
    
    class Meta:
        verbose_name = 'Сессия упражнения'
        verbose_name_plural = 'Сессии упражнений'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise_type.name} - {self.started_at.strftime('%d.%m.%Y %H:%M')}"


class GeneratedTextCache(models.Model):
    """Кэш сгенерированных текстов с вопросами"""
    
    DIFFICULTY_CHOICES = [
        (1, 'Лёгкий'),
        (2, 'Средний'),
        (3, 'Сложный'),
    ]
    
    text = models.TextField(verbose_name='Текст')
    questions = models.JSONField(verbose_name='Вопросы и ответы')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, verbose_name='Сложность')
    
    used_count = models.IntegerField(default=0, verbose_name='Сколько раз использован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_used = models.DateTimeField(auto_now=True, verbose_name='Последнее использование')
    
    class Meta:
        verbose_name = 'Кэш текста с вопросами'
        verbose_name_plural = 'Кэш текстов с вопросами'
    
    def __str__(self):
        return f"Текст {self.get_difficulty_display()} уровня (использован: {self.used_count})"


# ========== СИСТЕМА ДОСТИЖЕНИЙ ==========

class Achievement(models.Model):
    """Модель достижения"""
    
    CONDITION_TYPES = [
        ('tasks_completed', 'Выполнено заданий'),
        ('perfect_tasks', 'Заданий без ошибок'),
        ('level_reached', 'Достигнут уровень'),
        ('points_total', 'Всего очков опыта'),
        ('specific_task_perfect', 'Конкретное задание без ошибок'),
        ('hard_difficulty_task', 'Задание на высокой сложности'),
        ('specific_task_hard', 'Конкретное задание на высокой сложности'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    icon = models.CharField(max_length=50, default='bi-trophy-fill', verbose_name='Иконка')
    condition_type = models.CharField(max_length=50, choices=CONDITION_TYPES, verbose_name='Тип условия')
    condition_value = models.IntegerField(verbose_name='Значение условия')
    condition_extra = models.CharField(max_length=100, blank=True, null=True, verbose_name='Дополнительный параметр')
    reward_points = models.IntegerField(default=0, verbose_name='Награда (опыт)')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    
    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Выполненные достижения пользователя"""
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')
    
    class Meta:
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"