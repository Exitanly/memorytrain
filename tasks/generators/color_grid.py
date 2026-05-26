import random
from .base import BaseTaskGenerator

class ColorGridGenerator(BaseTaskGenerator):
    """Генератор для запоминания цветных клеток"""
    
    def generate(self):
        # Параметры в зависимости от сложности
        if self.difficulty == 1:  # Лёгкий
            grid_size = 2  # 2x2
            colors = [
                '#FF0000',  # Красный
                '#00FF00',  # Зелёный
                '#0000FF',  # Синий
                '#FFFF00',  # Жёлтый
            ]
        elif self.difficulty == 2:  # Средний
            grid_size = 3  # 3x3
            colors = [
                '#FF0000', '#00FF00', '#0000FF', '#FFFF00',  # Основные
                '#FF00FF', '#00FFFF', '#FFA500', '#800080',  # Дополнительные
                '#FFC0CB',  # Розовый
            ]
        else:  # Сложный
            grid_size = 4  # 4x4
            colors = [
                '#FF0000', '#00FF00', '#0000FF', '#FFFF00',
                '#FF00FF', '#00FFFF', '#FFA500', '#800080',
                '#FFC0CB', '#A52A2A', '#008080', '#000080',
                '#808000', '#800000', '#008000', '#C0C0C0',
            ]
        
        # Создаём сетку цветов (перемешиваем)
        grid_colors = random.sample(colors, grid_size * grid_size)
        
        # Создаём матрицу цветов для отображения
        color_matrix = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                row.append(grid_colors[i * grid_size + j])
            color_matrix.append(row)
        
        # Время на запоминание (2 секунды на клетку)
        max_time = (grid_size * grid_size) * 1.5
        self.max_time = int(max_time)
        
        return {
            'task_data': {
                'grid_size': grid_size,
                'color_matrix': color_matrix,
                'colors_list': colors,
            },
            'check_data': {
                'grid_size': grid_size,
                'color_matrix': color_matrix,
                'max_time': self.max_time,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """
        user_answer: матрица цветов, выбранных пользователем
        """
        try:
            if isinstance(user_answer, str):
                import json
                user_answer = json.loads(user_answer)
            
            correct_matrix = check_data['color_matrix']
            grid_size = check_data['grid_size']
            
            # Сравниваем клетки
            correct_count = 0
            for i in range(grid_size):
                for j in range(grid_size):
                    if user_answer[i][j] == correct_matrix[i][j]:
                        correct_count += 1
            
            total_cells = grid_size * grid_size
            is_correct = correct_count == total_cells
            
            if is_correct:
                return True, f"Правильно! Вы раскрасили все {total_cells} клеток правильно!"
            else:
                return False, f"Правильно раскрашено {correct_count} из {total_cells} клеток."
                
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            return False, "Ошибка проверки ответа"
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        if not is_correct:
            return 0
        
        base_points = {1: 15, 2: 20, 3: 30}[self.difficulty]
        max_time = getattr(self, 'max_time', 30)
        
        if time_spent < max_time * 0.5:
            bonus = 1.2
        elif time_spent < max_time * 0.7:
            bonus = 1.1
        else:
            bonus = 1.0
        
        score = int(base_points * bonus)
        return min(score, base_points + 10)