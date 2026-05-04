import random
from .base import BaseTaskGenerator

class PatternGridGenerator(BaseTaskGenerator):
    """Генератор заданий с паттерном на сетке"""
    
    def generate(self):
        sizes = {1: 3, 2: 4, 3: 5}
        cell_counts = {1: 3, 2: 5, 3: 8}
        
        grid_size = sizes[self.difficulty]
        cells_count = cell_counts[self.difficulty]
        
        total_cells = grid_size * grid_size
        pattern = sorted(random.sample(range(total_cells), cells_count))
        
        self.max_time = {1: 5, 2: 6, 3: 8}[self.difficulty]
        
        self.task_data = {
            'grid_size': grid_size,
            'pattern': pattern,
        }
        
        return {
            'task_data': {
                'grid_size': grid_size,
                'pattern': pattern,
            },
            'check_data': {
                'pattern': pattern,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """user_answer - список индексов, которые выбрал пользователь"""
        correct_pattern = check_data['pattern']
        
        if len(user_answer) != len(correct_pattern):
            return False, f"Нужно отметить {len(correct_pattern)} клеток"
        
        if sorted(user_answer) == correct_pattern:
            return True, "Правильно!"
        return False, "Неправильно. Попробуйте ещё раз!"