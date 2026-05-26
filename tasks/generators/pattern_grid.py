import random
from .base import BaseTaskGenerator

class PatternGridGenerator(BaseTaskGenerator):
    """Генератор для запоминания паттерна на сетке"""
    
    def generate(self):
        # Параметры в зависимости от сложности
        if self.difficulty == 1:  # Лёгкий
            grid_size = 3
            cells_count = 3
        elif self.difficulty == 2:  # Средний
            grid_size = 4
            cells_count = 5
        else:  # Сложный
            grid_size = 5
            cells_count = 8
        
        total_cells = grid_size * grid_size
        
        # Генерируем случайные позиции для зелёных клеток
        pattern = sorted(random.sample(range(total_cells), cells_count))
        
        # Время на запоминание (1 секунда на клетку + база)
        max_time = cells_count + 2
        self.max_time = max_time
        
        return {
            'task_data': {
                'grid_size': grid_size,
                'pattern': pattern,
                'cells_count': cells_count,
            },
            'check_data': {
                'grid_size': grid_size,
                'pattern': pattern,
                'cells_count': cells_count,
            },
            'max_time': max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """
        user_answer: список индексов клеток, которые выбрал пользователь
        """
        try:
            if isinstance(user_answer, str):
                import json
                user_answer = json.loads(user_answer)
            
            correct_pattern = check_data['pattern']
            cells_count = check_data['cells_count']
            
            # Проверяем количество
            if len(user_answer) != cells_count:
                return False, f"Вы выбрали {len(user_answer)} клеток, а нужно {cells_count}"
            
            # Сортируем и сравниваем
            user_sorted = sorted(user_answer)
            correct_sorted = sorted(correct_pattern)
            
            if user_sorted == correct_sorted:
                return True, f"Правильно! Вы запомнили все {cells_count} клеток!"
            else:
                # Подсчитываем правильные
                correct_count = len(set(user_sorted) & set(correct_sorted))
                return False, f"Правильно отмечено {correct_count} из {cells_count} клеток"
                
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            return False, "Ошибка проверки ответа"
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        if not is_correct:
            return 0
        
        base_points = {1: 10, 2: 15, 3: 20}[self.difficulty]
        max_time = getattr(self, 'max_time', 30)
        
        # Бонус за скорость
        if time_spent < max_time * 0.5:
            bonus = 1.3
        elif time_spent < max_time * 0.7:
            bonus = 1.15
        else:
            bonus = 1.0
        
        score = int(base_points * bonus)
        return min(score, base_points + 10)