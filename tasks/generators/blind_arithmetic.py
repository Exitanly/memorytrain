import random
from .base import BaseTaskGenerator

class BlindArithmeticGenerator(BaseTaskGenerator):
    """Генератор для слепого арифметического действия"""
    
    def generate(self):
        # Параметры в зависимости от сложности
        if self.difficulty == 1:  # Лёгкий
            num_range = (1, 20)
            operations = ['+', '-']
        elif self.difficulty == 2:  # Средний
            num_range = (10, 99)
            operations = ['+', '-', '*']
        else:  # Сложный
            num_range = (100, 999)
            operations = ['+', '-', '*', '/']
        
        # Генерируем два числа
        num1 = random.randint(num_range[0], num_range[1])
        num2 = random.randint(num_range[0], num_range[1])
        
        # Для деления делаем так, чтобы результат был целым
        operation = random.choice(operations)
        if operation == '/' and num2 != 0:
            # Делаем num1 кратным num2
            num1 = num2 * random.randint(1, 10)
        
        # Вычисляем результат
        if operation == '+':
            result = num1 + num2
            op_symbol = '+'
            op_name = 'сложение'
        elif operation == '-':
            result = num1 - num2
            op_symbol = '-'
            op_name = 'вычитание'
        elif operation == '*':
            result = num1 * num2
            op_symbol = '×'
            op_name = 'умножение'
        else:  # '/'
            result = num1 // num2
            op_symbol = '÷'
            op_name = 'деление'
        
        # Время на запоминание
        self.max_time = {1: 3, 2: 4, 3: 5}[self.difficulty]
        
        return {
            'task_data': {
                'num1': num1,
                'num2': num2,
                'op_symbol': op_symbol,
                'op_name': op_name,
            },
            'check_data': {
                'result': result,
                'op_name': op_name,
            },
            'max_time': self.max_time,
        }
    
    def check_answer(self, user_answer, check_data):
        """Проверка ответа пользователя"""
        try:
            user_result = int(user_answer)
            correct_result = check_data['result']
            
            if user_result == correct_result:
                return True, f"Правильно! Результат = {correct_result}"
            else:
                return False, f"Неправильно. Правильный ответ: {correct_result}"
        except:
            return False, "Введите целое число"