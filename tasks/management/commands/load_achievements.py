from django.core.management.base import BaseCommand
from tasks.models import Achievement

class Command(BaseCommand):
    help = 'Загружает список достижений'
    
    def handle(self, *args, **options):
        achievements = [
            # 1. Первые шаги
            {'name': 'Первые шаги', 'description': 'Выполни одно задание', 'icon': 'bi-footsteps', 
             'condition_type': 'tasks_completed', 'condition_value': 1, 'reward_points': 10, 'order': 1},
            
            # 2. Уже лучше
            {'name': 'Уже лучше', 'description': 'Достигни 5 уровня', 'icon': 'bi-arrow-up-circle', 
             'condition_type': 'level_reached', 'condition_value': 5, 'reward_points': 50, 'order': 2},
            
            # 3. Я помню
            {'name': 'Я помню', 'description': 'Выполни 15 заданий', 'icon': 'bi-journal-bookmark-fill', 
             'condition_type': 'tasks_completed', 'condition_value': 15, 'reward_points': 75, 'order': 3},
            
            # 4. Художник
            {'name': 'Художник', 'description': 'Выполни задание "Цветные клетки" без ошибок', 'icon': 'bi-palette-fill', 
             'condition_type': 'specific_task_perfect', 'condition_value': 1, 'condition_extra': 'color-grid', 'reward_points': 50, 'order': 4},
            
            # 5. Всё мне
            {'name': 'Всё мне', 'description': 'Собери 500 очков опыта', 'icon': 'bi-cash-stack', 
             'condition_type': 'points_total', 'condition_value': 500, 'reward_points': 100, 'order': 5},
            
            # 6. Я помню всё
            {'name': 'Я помню всё', 'description': 'Достигни 10 уровня', 'icon': 'bi-star-fill', 
             'condition_type': 'level_reached', 'condition_value': 10, 'reward_points': 100, 'order': 6},
            
            # 7. Мастер
            {'name': 'Мастер', 'description': 'Выполни любое задание на высокой сложности', 'icon': 'bi-trophy-fill', 
             'condition_type': 'hard_difficulty_task', 'condition_value': 1, 'reward_points': 75, 'order': 7},
            
            # 8. Шишкин
            {'name': 'Шишкин', 'description': 'Выполни задание "Цветные клетки" на высокой сложности', 'icon': 'bi-brush-fill', 
             'condition_type': 'specific_task_hard', 'condition_value': 1, 'condition_extra': 'color-grid', 'reward_points': 100, 'order': 8},
            
            # 9. Без тормозов
            {'name': 'Без тормозов', 'description': 'Собери 2000 очков опыта', 'icon': 'bi-lightning-charge-fill', 
             'condition_type': 'points_total', 'condition_value': 2000, 'reward_points': 150, 'order': 9},
            
            # 10. Вспомнить всё
            {'name': 'Вспомнить всё', 'description': 'Достигни 50 уровня', 'icon': 'bi-gem', 
             'condition_type': 'level_reached', 'condition_value': 50, 'reward_points': 500, 'order': 10},
            
            # 11. Мегамозг
            {'name': 'Мегамозг', 'description': 'Выполни 100 заданий', 'icon': 'bi-cpu-fill', 
             'condition_type': 'tasks_completed', 'condition_value': 100, 'reward_points': 200, 'order': 11},
            
            # 12. Идеальная память
            {'name': 'Идеальная память', 'description': 'Выполни 30 заданий без ошибок', 'icon': 'bi-award-fill', 
             'condition_type': 'perfect_tasks', 'condition_value': 30, 'reward_points': 250, 'order': 12},
        ]
        
        for ach_data in achievements:
            obj, created = Achievement.objects.get_or_create(
                name=ach_data['name'],
                defaults=ach_data
            )
            if created:
                self.stdout.write(f'✓ Создано: {obj.name}')
            else:
                self.stdout.write(f'○ Существует: {obj.name}')
        
        self.stdout.write(self.style.SUCCESS('✅ Достижения загружены!'))