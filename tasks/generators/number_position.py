import random
from .base import BaseTaskGenerator

class NumberPositionGenerator(BaseTaskGenerator):
    """Генератор для запоминания расположения чисел"""
    
    def generate(self):
        # Параметры в зависимости от сложности
        if self.difficulty == 1:  # Лёгкий
            grid_size = 3
            numbers_count = 4
        elif self.difficulty == 2:  # Средний
            grid_size = 4
            numbers_count = 6
        else:  # Сложный
            grid_size = 5
            numbers_count = 10
        
        total_cells = grid_size * grid_size
        
        # Генерируем случайные позиции для чисел
        positions = random.sample(range(total_cells), numbers_count)
        
        # Создаём последовательность: номер числа -> позиция
        sequence = {}
        for i, pos in enumerate(positions, 1):
            sequence[str(i)] = pos
        
        # Время на запоминание
        max_time = numbers_count * 1.5
        self.max_time = int(max_time)
        
        return {
            'task_data': {
                'grid_size': grid_size,
                'numbers_count': numbers_count,
                'sequence': sequence,
            },
            'check_data': {
                'grid_size': grid_size,
                'numbers_count': numbers_count,
                'sequence': sequence,
                'max_time': self.max_time,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        try:
            if isinstance(user_answer, str):
                if user_answer:
                    import json
                    user_answer = json.loads(user_answer)
                else:
                    return False, "Нет данных ответа"
            
            if not user_answer:
                return False, "Вы не нажали ни одной клетки"
            
            sequence = check_data['sequence']
            numbers_count = check_data['numbers_count']
            
            # Ожидаемая последовательность позиций
            expected_order = [sequence[str(i)] for i in range(1, numbers_count + 1)]
            
            # Сравниваем
            is_correct = user_answer == expected_order
            
            if is_correct:
                return True, f"Правильно! Вы запомнили все {numbers_count} чисел!"
            else:
                correct_count = 0
                for i, pos in enumerate(user_answer):
                    if i < len(expected_order) and pos == expected_order[i]:
                        correct_count += 1
                    else:
                        break
                
                return False, f"Неправильно. Вы правильно указали {correct_count} из {numbers_count} позиций."
                
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            import traceback
            traceback.print_exc()
            return False, "Ошибка проверки ответа"
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        if not is_correct:
            return 0
        
        base_points = {1: 15, 2: 20, 3: 30}[self.difficulty]
        max_time = getattr(self, 'max_time', 30)
        
        if time_spent < max_time * 0.5:
            bonus = 1.2
        elif time_spent < max_time * 0.8:
            bonus = 1.1
        else:
            bonus = 1.0
        
        score = int(base_points * bonus)
        return min(score, base_points + 10)