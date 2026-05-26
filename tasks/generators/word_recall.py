import random
from .base import BaseTaskGenerator

class WordRecallGenerator(BaseTaskGenerator):
    """Генератор для запоминания слов с выбором"""
    
    def generate(self):
        # Базы слов по сложности
        if self.difficulty == 1:  # Лёгкий
            words_count = 5
            extra_words_count = 2
            word_pool = [
                'кот', 'дом', 'лес', 'река', 'гора', 'море', 'сон', 'день',
                'ночь', 'хлеб', 'вода', 'огонь', 'ветер', 'друг', 'мама', 'папа'
            ]
        elif self.difficulty == 2:  # Средний
            words_count = 7
            extra_words_count = 3
            word_pool = [
                'компьютер', 'телефон', 'библиотека', 'университет', 'ресторан',
                'путешествие', 'впечатление', 'достопримечательность', 'оборудование',
                'рекомендация', 'удовольствие', 'правительство', 'образование'
            ]
        else:  # Сложный
            words_count = 10
            extra_words_count = 4
            word_pool = [
                'электрокардиограмма', 'рентгенорадиолюминесценция', 'фототелеграмма',
                'гидроэлектростанция', 'макрофотография', 'стереофотограмметрия',
                'электроэнцефалограмма', 'ультрамикроскопический', 'сельскохозяйственный'
            ]
        
        # Выбираем слова для запоминания
        memory_words = random.sample(word_pool, words_count)
        
        # Выбираем лишние слова (которых нет в memory_words)
        available_extra = [w for w in word_pool if w not in memory_words]
        extra_words = random.sample(available_extra, extra_words_count)
        
        # Все слова для выбора (перемешиваем)
        all_choices = memory_words + extra_words
        random.shuffle(all_choices)
        
        # Время на запоминание (2 секунды на слово)
        max_time = words_count * 2
        self.max_time = max_time  # ← ДОБАВЬ ЭТУ СТРОКУ
        
        return {
            'task_data': {
                'memory_words': memory_words,
                'all_choices': all_choices,
                'words_count': words_count,
                'extra_words_count': extra_words_count,
            },
            'check_data': {
                'memory_words': memory_words,
                'words_count': words_count,
                'max_time': max_time,  # ← ДОБАВЬ ЭТУ СТРОКУ (опционально)
            },
            'max_time': max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """
        user_answer: список выбранных пользователем слов
        """
        try:
            if isinstance(user_answer, str):
                import json
                user_answer = json.loads(user_answer)
            
            memory_words = set(check_data['memory_words'])
            user_words = set(user_answer)
            
            # Правильные ответы: все слова из memory_words, без лишних
            is_correct = user_words == memory_words
            
            if is_correct:
                return True, f"Правильно! Вы запомнили все {len(memory_words)} слов!"
            else:
                # Подсчитываем правильные и лишние
                correct_found = len(user_words & memory_words)
                extra_selected = len(user_words - memory_words)
                missing = len(memory_words - user_words)
                
                return False, f"Найдено {correct_found} из {len(memory_words)} слов. Лишних: {extra_selected}. Пропущено: {missing}."
                
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            return False, "Ошибка проверки ответа"
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        if not is_correct:
            return 0
        
        base_points = {1: 10, 2: 15, 3: 20}[self.difficulty]
        
        # Используем self.max_time
        max_time = getattr(self, 'max_time', 30)
        
        # Бонус за скорость
        if time_spent < max_time * 0.5:
            bonus = 1.2
        elif time_spent < max_time * 0.7:
            bonus = 1.1
        else:
            bonus = 1.0
        
        score = int(base_points * bonus)
        return min(score, base_points + 10)