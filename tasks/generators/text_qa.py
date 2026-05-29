from .base import BaseTaskGenerator
from ..services.text_generator import generator as text_generator

class TextQAGenerator(BaseTaskGenerator):
    """Генератор для вопросов по тексту (гибридный)"""
    
    def generate(self, force_new=False, skip_generation=False):
        """
        force_new: принудительно генерировать новый текст
        skip_generation: не генерировать новый текст (использовать сохранённый)
        """
        if skip_generation and hasattr(self, '_cached_task'):
            return self._cached_task
        
        text_data = text_generator.get_text(self.difficulty, force_new=force_new)
        
        task = {
            'task_data': {
                'text': text_data['text'],
                'questions': text_data['questions'],
                'total_questions': len(text_data['questions']),
                'text_id': text_data.get('id'),
            },
            'check_data': {
                'questions': text_data['questions'],
                'text_id': text_data.get('id'),
            },
            'max_time': 0,
        }
        
        # Кэшируем задание
        self._cached_task = task
        return task
    
    def get_cached_task(self):
        """Возвращает кэшированное задание"""
        return getattr(self, '_cached_task', None)
    
    def check_answer(self, user_answer, check_data):
        try:
            if isinstance(user_answer, str):
                import json
                user_answer = json.loads(user_answer)
            
            questions = check_data['questions']
            
            correct_count = 0
            results = []
            user_answers = []
            
            for i, (q, user_ans) in enumerate(zip(questions, user_answer)):
                correct_answer = q['answer'].lower().strip()
                user_response = str(user_ans).lower().strip()
                user_answers.append(user_response)
                
                if correct_answer in user_response or user_response in correct_answer:
                    correct_count += 1
                    results.append(True)
                else:
                    results.append(False)
            
            total = len(questions)
            is_correct = correct_count == total
            
            # Сохраняем детали ответа для шаблона
            self.check_results = {
                'is_correct': is_correct,
                'correct_count': correct_count,
                'total': total,
                'results': results,
                'user_answers': user_answers,
                'text_id': check_data.get('text_id'),
            }
            
            if is_correct:
                return True, f"Правильно! {correct_count} из {total}"
            else:
                return False, f"Правильно: {correct_count} из {total}"
                
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            return False, "Ошибка проверки ответов"
    
    def calculate_score(self, is_correct, time_spent, attempts=1):
        if not is_correct:
            return 0
        return {1: 15, 2: 20, 3: 25}[self.difficulty]