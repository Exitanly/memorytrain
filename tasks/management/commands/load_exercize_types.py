from django.core.management.base import BaseCommand
from tasks.models import ExerciseType

class Command(BaseCommand):
    help = 'Загружает типы упражнений в базу данных'
    
    def handle(self, *args, **options):
        exercises = [
            # Визуальная память
            {
                'name': 'Карточки (Memo)',
                'slug': 'memory-cards',
                'category': 'visual',
                'description': 'Найдите все пары одинаковых карточек. Тренирует визуальную память и внимание.',
                'instruction': 'Переворачивайте карточки по две. Найдите все совпадающие пары.',
                'icon': 'bi-grid-3x3-gap-fill',
                'generator_class': 'MemoryCardsGenerator',
                'order': 1,
            },
            {
                'name': 'Паттерн на сетке',
                'slug': 'pattern-grid',
                'category': 'visual',
                'description': 'Запомните расположение зелёных клеток и повторите их.',
                'instruction': 'У вас есть несколько секунд, чтобы запомнить паттерн. Затем отметьте те же клетки.',
                'icon': 'bi-grid',
                'generator_class': 'PatternGridGenerator',
                'order': 2,
            },
            {
                'name': 'Цветные клетки',
                'slug': 'color-grid',
                'category': 'visual',
                'description': 'Запомните расположение цветов в сетке и восстановите их.',
                'instruction': 'Запомните, где какой цвет. Затем раскрасьте клетки правильно.',
                'icon': 'bi-palette',
                'generator_class': 'ColorGridGenerator',
                'order': 3,
            },
            
            # Числовая память
            {
                'name': 'Последовательность чисел',
                'slug': 'number-sequence',
                'category': 'number',
                'description': 'Запомните последовательность чисел и повторите её.',
                'instruction': 'Вам покажут числа. Запомните порядок и введите их.',
                'icon': 'bi-123',
                'generator_class': 'NumberSequenceGenerator',
                'order': 1,
            },
            {
                'name': 'Расположение чисел',
                'slug': 'number-position',
                'category': 'number',
                'description': 'Запомните, где появлялись числа, и нажмите на них в правильном порядке.',
                'instruction': 'Числа будут появляться в разных местах. Запомните их расположение и последовательность.',
                'icon': 'bi-pin-map-fill',
                'generator_class': 'NumberPositionGenerator',
                'order': 2,
            },
            {
                'name': 'Слепое действие',
                'slug': 'blind-arithmetic',
                'category': 'number',
                'description': 'Запомните два числа, а затем выполните с ними арифметическое действие.',
                'instruction': 'Запомните показанные числа. Затем решите пример.',
                'icon': 'bi-calculator-fill',
                'generator_class': 'BlindArithmeticGenerator',
                'order': 3,
            },
            
            # Текстовая память
            {
                'name': 'Запоминание слов',
                'slug': 'word-recall',
                'category': 'text',
                'description': 'Запомните слова и выберите только те, которые видели.',
                'instruction': 'Вам покажут список слов. Затем выберите только те, которые были в списке.',
                'icon': 'bi-file-text-fill',
                'generator_class': 'WordRecallGenerator',
                'order': 1,
            },
            {
                'name': 'Найди лишнее слово',
                'slug': 'odd-word',
                'category': 'text',
                'description': 'Запомните слова и найдите то, которого не было в списке.',
                'instruction': 'Запомните слова. Затем найдите одно новое слово, которого не было.',
                'icon': 'bi-question-octagon-fill',
                'generator_class': 'OddWordGenerator',
                'order': 2,
            },
            {
                'name': 'Вопросы по тексту',
                'slug': 'text-questions',
                'category': 'text',
                'description': 'Прочитайте текст и ответьте на вопросы по нему.',
                'instruction': 'Внимательно прочитайте текст. Затем ответьте на вопросы.',
                'icon': 'bi-chat-text-fill',
                'generator_class': 'TextQAGenerator',
                'order': 3,
            },
        ]
        
        for ex in exercises:
            obj, created = ExerciseType.objects.get_or_create(
                slug=ex['slug'],
                defaults=ex
            )
            if created:
                self.stdout.write(f'✓ Создан: {obj.name}')
            else:
                self.stdout.write(f'○ Уже существует: {obj.name}')
        
        self.stdout.write(self.style.SUCCESS('✅ Типы упражнений загружены!'))