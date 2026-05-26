import random
import json
from .base import BaseTaskGenerator

class MemoryCardsGenerator(BaseTaskGenerator):
    """Генератор для игры в пары (Memo)"""
    
    def generate(self):
        # Набор иконок/символов для карточек
        icons = {
            1: ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊'],  # 6 пар для лёгкого
            2: ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼'],  # 8 пар
            3: ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮'],  # 12 пар
        }
        
        # Количество пар в зависимости от сложности
        pairs_count = {1: 6, 2: 8, 3: 12}[self.difficulty]
        
        # Выбираем случайные иконки
        available_icons = icons[self.difficulty]
        selected_icons = random.sample(available_icons, pairs_count)
        
        # Создаём пары и перемешиваем
        cards = selected_icons * 2
        random.shuffle(cards)
        
        self.max_time = 0  # 0 означает "без ограничения"
        
        return {
            'task_data': {
                'cards': cards,
                'pairs_count': pairs_count,
                'grid_cols': 4 if pairs_count <= 8 else 6,
            },
            'check_data': {
                'pairs_count': pairs_count,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """Проверка ответа пользователя"""
        try:
            print(f"DEBUG: Получен user_answer: {user_answer}")
            print(f"DEBUG: Тип user_answer: {type(user_answer)}")
            
            # Если user_answer - строка, парсим JSON
            if isinstance(user_answer, str):
                user_answer = json.loads(user_answer)
                print(f"DEBUG: После парсинга: {user_answer}")
            
            # Извлекаем данные
            matched_pairs = user_answer.get('matched_pairs', 0)
            total_pairs = user_answer.get('total_pairs', check_data.get('pairs_count', 0))
            moves = user_answer.get('moves', 0)
            completed = user_answer.get('completed', False)
            
            print(f"DEBUG: matched_pairs={matched_pairs}, total_pairs={total_pairs}, completed={completed}")
            
            # Проверяем
            if not completed:
                return False, "Игра не завершена. Найдите все пары!"
            
            if matched_pairs == total_pairs and matched_pairs > 0:
                self.moves_count = moves
                return True, f"Поздравляю! Вы нашли все {total_pairs} пар за {moves} ходов!"
            else:
                remaining = total_pairs - matched_pairs
                return False, f"Найдено {matched_pairs} пар из {total_pairs}. Осталось {remaining} пар."
                
        except Exception as e:
            print(f"DEBUG: Ошибка: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Ошибка проверки: {str(e)}"
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        if not is_correct:
            return 0
        
        base_points = {1: 15, 2: 20, 3: 25}[self.difficulty]
        
        moves = getattr(self, 'moves_count', 20)
        pairs_count = {1: 6, 2: 8, 3: 12}[self.difficulty]
        
        # Идеальное количество ходов = количество пар * 2
        min_moves = pairs_count * 2
        
        if moves <= min_moves:
            efficiency = 1.0
        else:
            efficiency = max(0, 1 - (moves - min_moves) / min_moves)
        
        score = int(base_points * (0.5 + efficiency * 0.5))
        
        return max(base_points // 2, min(base_points, score))