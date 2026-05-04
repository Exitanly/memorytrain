import random
from .base import BaseTaskGenerator

class NumberSequenceGenerator(BaseTaskGenerator):
    """Генератор заданий с последовательностью чисел"""
    
    def generate(self):
        lengths = {1: 5, 2: 7, 3: 10}
        ranges = {1: (0, 9), 2: (10, 99), 3: (100, 999)}
        
        length = lengths[self.difficulty]
        low, high = ranges[self.difficulty]
        
        numbers = [random.randint(low, high) for _ in range(length)]
        
        self.max_time = {1: 5, 2: 7, 3: 10}[self.difficulty]
        
        return {
            'task_data': {
                'numbers': numbers,
            },
            'check_data': {
                'numbers': numbers,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """user_answer - строка с числами через запятую"""
        try:
            if isinstance(user_answer, str):
                user_numbers = [int(x.strip()) for x in user_answer.split(',')]
            else:
                user_numbers = user_answer
            
            correct = check_data['numbers']
            
            if user_numbers == correct:
                return True, "Правильно!"
            return False, f"Неправильно. Правильная последовательность: {', '.join(map(str, correct))}"
        except:
            return False, "Неверный формат. Введите числа через запятую"