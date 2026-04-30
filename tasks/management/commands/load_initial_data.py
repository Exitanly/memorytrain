from django.core.management.base import BaseCommand
from tasks.models import TaskCategory, Task

class Command(BaseCommand):
    help = 'Загружает начальные задания'

    def handle(self, *args, **options):
        # Создаём категории
        categories = {
            'visual': {'name': 'Визуальная память', 'description': 'Запоминание изображений и паттернов', 'icon': 'bi-eye'},
            'text': {'name': 'Текстовая память', 'description': 'Запоминание текстов и слов', 'icon': 'bi-file-text'},
            'number': {'name': 'Числовая память', 'description': 'Запоминание чисел и последовательностей', 'icon': 'bi-123'},
            'pattern': {'name': 'Паттерны', 'description': 'Запоминание последовательностей', 'icon': 'bi-grid-3x3'},
        }
        
        for key, data in categories.items():
            category, created = TaskCategory.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'icon': data['icon']
                }
            )
            self.stdout.write(f'{"Создана" if created else "Найдена"} категория: {category.name}')
        
        # Получаем категории для использования
        visual_cat = TaskCategory.objects.get(name='Визуальная память')
        text_cat = TaskCategory.objects.get(name='Текстовая память')
        number_cat = TaskCategory.objects.get(name='Числовая память')
        
        # Создаём задания
        tasks_data = [
            # Визуальные задания
            {
                'title': 'Запомни цвет',
                'description': 'Запомните цвет квадрата и выберите его из предложенных',
                'category': visual_cat,
                'task_type': 'visual',
                'difficulty': 1,
                'base_points': 10,
                'task_data': {'colors': ['red', 'blue', 'green', 'yellow', 'purple', 'orange'], 'question': 'Какой цвет был показан?'}
            },
            {
                'title': 'Паттерн сетки',
                'description': 'Запомните расположение закрашенных клеток в сетке 3x3',
                'category': visual_cat,
                'task_type': 'visual',
                'difficulty': 2,
                'base_points': 15,
                'task_data': {'grid_size': 3, 'cells': [0, 4, 8]}
            },
            {
                'title': 'Сложный паттерн',
                'description': 'Запомните расположение закрашенных клеток в сетке 4x4',
                'category': visual_cat,
                'task_type': 'visual',
                'difficulty': 3,
                'base_points': 20,
                'task_data': {'grid_size': 4, 'cells': [1, 5, 6, 10, 14]}
            },
            
            # Текстовые задания
            {
                'title': 'Список слов',
                'description': 'Запомните список из 5 слов',
                'category': text_cat,
                'task_type': 'text',
                'difficulty': 1,
                'base_points': 10,
                'task_data': {'words': ['яблоко', 'книга', 'дом', 'солнце', 'река']}
            },
            {
                'title': 'Цепочка слов',
                'description': 'Запомните последовательность из 7 слов',
                'category': text_cat,
                'task_type': 'text',
                'difficulty': 2,
                'base_points': 15,
                'task_data': {'words': ['утро', 'кофе', 'работа', 'обед', 'кино', 'вечер', 'сон']}
            },
            {
                'title': 'Текст для запоминания',
                'description': 'Запомните короткий текст',
                'category': text_cat,
                'task_type': 'text',
                'difficulty': 3,
                'base_points': 20,
                'task_data': {'text': 'В лесу родилась ёлочка, в лесу она росла. Зимой и летом стройная, зелёная была.'}
            },
            
            # Числовые задания
            {
                'title': 'Последовательность чисел',
                'description': 'Запомните последовательность из 5 чисел',
                'category': number_cat,
                'task_type': 'number',
                'difficulty': 1,
                'base_points': 10,
                'task_data': {'numbers': [5, 2, 8, 3, 9]}
            },
            {
                'title': 'Длинная последовательность',
                'description': 'Запомните последовательность из 8 чисел',
                'category': number_cat,
                'task_type': 'number',
                'difficulty': 2,
                'base_points': 15,
                'task_data': {'numbers': [7, 3, 9, 2, 5, 8, 1, 4]}
            },
            {
                'title': 'Сложная последовательность',
                'description': 'Запомните последовательность из 10 чисел',
                'category': number_cat,
                'task_type': 'number',
                'difficulty': 3,
                'base_points': 20,
                'task_data': {'numbers': [9, 4, 7, 2, 8, 5, 1, 6, 3, 0]}
            },
            # Паттерны
            {
                'title': 'Запомни паттерн',
                'description': 'Запомните расположение крестиков в сетке 3x3 и повторите',
                'category': TaskCategory.objects.get(name='Паттерны'),
                'task_type': 'pattern',
                'difficulty': 1,
                'base_points': 10,
                'task_data': {'grid_size': 3, 'pattern': [0, 4, 8]}
            },
            {
                'title': 'Сложный паттерн',
                'description': 'Запомните расположение крестиков в сетке 4x4',
                'category': TaskCategory.objects.get(name='Паттерны'),
                'task_type': 'pattern',
                'difficulty': 2,
                'base_points': 15,
                'task_data': {'grid_size': 4, 'pattern': [0, 5, 6, 10, 15]}
            },
        ]
        
        for task_data in tasks_data:
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                defaults=task_data
            )
            self.stdout.write(f'{"Создано" if created else "Найдено"} задание: {task.title}')
        
        self.stdout.write(self.style.SUCCESS('Начальные данные успешно загружены!'))