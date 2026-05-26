import random
from .base import BaseTaskGenerator

class OddWordGenerator(BaseTaskGenerator):
    """Генератор для игры 'Найди лишнее слово'"""
    
    def generate(self):
        # Базы слов по сложности
        if self.difficulty == 1:  # Лёгкий
            words_count = 5
            word_pool = [
                'яблоко', 'груша', 'банан', 'апельсин', 'мандарин',
                'кот', 'собака', 'птица', 'рыба', 'хомяк',
                'стол', 'стул', 'шкаф', 'кровать', 'диван'
            ]
        elif self.difficulty == 2:  # Средний
            words_count = 6
            word_pool = [
                'компьютер', 'ноутбук', 'планшет', 'телефон', 'монитор', 'клавиатура',
                'врач', 'учитель', 'инженер', 'строитель', 'водитель', 'повар',
                'берлин', 'париж', 'лондон', 'мадрид', 'рим', 'венекция'
            ]
        else:  # Сложный
            words_count = 8
            word_pool = [
                'рекомендация', 'удовольствие', 'правительство', 'образование',
                'достопримечательность', 'оборудование', 'путешествие', 'впечатление',
                'электрокардиограмма', 'рентгенорадиолюминесценция', 'фототелеграмма',
                'гидроэлектростанция', 'макрофотография', 'стереофотограмметрия'
            ]
        
        # Выбираем случайную тему/категорию (берём слова из одной группы)
        # Для простоты берём случайный блок из 8 слов
        available_words = random.sample(word_pool, words_count + 1)
        
        # Слова для запоминания (первые words_count слов)
        memory_words = available_words[:words_count]
        
        # Лишнее слово (последнее)
        odd_word = available_words[words_count]
        
        # Все слова для выбора (перемешиваем)
        all_choices = memory_words + [odd_word]
        random.shuffle(all_choices)
        
        # Время на запоминание (1.5 секунды на слово)
        max_time = words_count * 1.5
        self.max_time = int(max_time)
        
        return {
            'task_data': {
                'memory_words': memory_words,
                'all_choices': all_choices,
                'words_count': words_count,
            },
            'check_data': {
                'memory_words': memory_words,
                'odd_word': odd_word,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """
        user_answer: выбранное пользователем слово (лишнее)
        """
        try:
            if isinstance(user_answer, str):
                import json
                user_answer = json.loads(user_answer)
            
            odd_word = check_data['odd_word']
            
            is_correct = user_answer == odd_word
            
            if is_correct:
                return True, f"Правильно! Слово '{odd_word}' действительно лишнее!"
            else:
                return False, f"Неправильно. Лишнее слово: '{odd_word}'"
                
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            return False, "Ошибка проверки ответа"
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        if not is_correct:
            return 0
        
        base_points = {1: 15, 2: 20, 3: 25}[self.difficulty]
        max_time = getattr(self, 'max_time', 30)
        
        if time_spent < max_time * 0.5:
            bonus = 1.2
        elif time_spent < max_time * 0.7:
            bonus = 1.1
        else:
            bonus = 1.0
        
        score = int(base_points * bonus)
        return min(score, base_points + 10)