import random
from .base import BaseTaskGenerator

class MemoryCardsGenerator(BaseTaskGenerator):
    """Генератор для игры в пары (Memo)"""
    
    def generate(self):
        # Набор иконок/символов для карточек
        icons = {
            1: ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼'],  # 8 пар для лёгкого
            2: ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮'],  # 12 пар
            3: ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', 
                 '🐸', '🐵', '🐔', '🐧'],  # 16 пар
        }
        
        # Количество пар в зависимости от сложности
        pairs_count = {1: 6, 2: 8, 3: 12}[self.difficulty]
        
        # Выбираем случайные иконки
        available_icons = icons[self.difficulty]
        selected_icons = random.sample(available_icons, pairs_count)
        
        # Создаём пары и перемешиваем
        cards = selected_icons * 2  # Две копии каждой иконки
        random.shuffle(cards)
        
        # Время на игру не ограничено (пользователь сам завершает)
        self.max_time = 0  # 0 означает "без ограничения"
        
        self.task_data = {
            'cards': cards,
            'pairs_count': pairs_count,
            'grid_cols': 4 if pairs_count <= 8 else 6,  # Адаптивная сетка
        }
        
        return {
            'task_data': self.task_data,
            'check_data': {
                'cards': cards,
                'pairs_count': pairs_count,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """
        user_answer: список попыток пользователя в формате
        [{'card1': 0, 'card2': 5, 'matched': True}, ...]
        """
        try:
            # Проверяем, что все пары найдены
            cards = check_data['cards']
            pairs_count = check_data['pairs_count']
            
            # Подсчитываем количество найденных пар
            matched_pairs = set()
            for attempt in user_answer:
                if attempt.get('matched') and 'card1' in attempt and 'card2' in attempt:
                    value1 = cards[attempt['card1']]
                    value2 = cards[attempt['card2']]
                    if value1 == value2:
                        matched_pairs.add(value1)
            
            # Все ли пары найдены?
            is_correct = len(matched_pairs) == pairs_count
            
            if is_correct:
                # Бонус за количество ходов (чем меньше, тем лучше)
                moves = len(user_answer)
                move_bonus = max(0, 1 - (moves - pairs_count) / pairs_count * 0.3)
                return True, f"Поздравляю! Вы нашли все {pairs_count} пар за {moves} ходов!"
            else:
                remaining = pairs_count - len(matched_pairs)
                return False, f"Найдено {len(matched_pairs)} пар из {pairs_count}. Осталось {remaining} пар."
        except:
            return False, "Ошибка проверки. Пожалуйста, завершите игру."
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        """Переопределяем для особого расчёта (по количеству ходов)"""
        if not is_correct:
            return 0
        
        base_points = {1: 15, 2: 20, 3: 25}[self.difficulty]
        
        # Получаем количество ходов из сессии
        moves = getattr(self, 'moves_count', 20)
        pairs_count = {1: 6, 2: 8, 3: 12}[self.difficulty]
        
        # Бонус за эффективность (минимальное количество ходов = pairs_count * 2)
        min_moves = pairs_count * 2
        efficiency = max(0, 1 - (moves - min_moves) / min_moves)
        
        score = int(base_points * (0.7 + efficiency * 0.3))
        return max(base_points // 2, min(base_points, score))