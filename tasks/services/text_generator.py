import random
import json
import requests
from django.conf import settings
from ..models import GeneratedTextCache

class HybridTextGenerator:
    """Гибридный генератор текстов"""
    
    STATIC_TEXTS = {
        1: [  # Лёгкие
            {
                'text': 'У кота Мурзика была любимая миска. Каждое утро он ждал корм. Однажды хозяин забыл покормить кота. Мурзик сидел у пустой миски и грустно мяукал.',
                'questions': [
                    {'question': 'Как звали кота?', 'answer': 'Мурзик'},
                    {'question': 'Что стояло у кота?', 'answer': 'миска'},
                ]
            },
            {
                'text': 'Маша и Петя пошли в лес за грибами. Маша нашла 5 белых грибов. Петя нашёл 3 подберёзовика. Домой дети принесли полную корзину грибов.',
                'questions': [
                    {'question': 'Сколько белых грибов нашла Маша?', 'answer': '5'},
                    {'question': 'Что нашёл Петя?', 'answer': 'подберёзовики'},
                ]
            },
            {
                'text': 'В зоопарке жил жираф по имени Гоша. Он был очень высоким и любил есть листья с верхних веток. Каждый день к Гоше приходили дети и кормили его морковкой.',
                'questions': [
                    {'question': 'Как звали жирафа?', 'answer': 'Гоша'},
                    {'question': 'Что любил есть жираф?', 'answer': 'листья'},
                ]
            },
        ],
        2: [  # Средние
            {
                'text': 'Байкал - самое глубокое озеро на планете. Его максимальная глубина достигает 1642 метров. В озере обитает более 2600 видов животных и растений, многие из которых не встречаются больше нигде в мире.',
                'questions': [
                    {'question': 'Какое озеро самое глубокое?', 'answer': 'Байкал'},
                    {'question': 'Какая максимальная глубина Байкала?', 'answer': '1642 метра'},
                ]
            },
            {
                'text': 'Александр Сергеевич Пушкин родился в 1799 году в Москве. Он написал множество известных произведений, среди которых "Евгений Онегин", "Руслан и Людмила" и "Капитанская дочка". Поэт погиб на дуэли в 1837 году.',
                'questions': [
                    {'question': 'Где родился Пушкин?', 'answer': 'Москва'},
                    {'question': 'В каком году погиб Пушкин?', 'answer': '1837'},
                ]
            },
        ],
        3: [  # Сложные
            {
                'text': 'В 1961 году Юрий Гагарин стал первым человеком в космосе. Его корабль "Восток-1" совершил один оборот вокруг Земли за 108 минут. Максимальная высота полёта составила 327 километров.',
                'questions': [
                    {'question': 'Кто стал первым космонавтом?', 'answer': 'Юрий Гагарин'},
                    {'question': 'Сколько минут длился полёт?', 'answer': '108 минут'},
                ]
            },
            {
                'text': 'Компьютерный вирус "Stuxnet" был обнаружен в 2010 году. Он поражал промышленные системы управления и нанёс значительный ущерб иранской ядерной программе. Вирус распространялся через USB-накопители.',
                'questions': [
                    {'question': 'В каком году был обнаружен Stuxnet?', 'answer': '2010'},
                    {'question': 'Как распространялся вирус?', 'answer': 'USB-накопители'},
                ]
            },
        ]
    }
    
    def __init__(self):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
        self.use_api = True  # Можно временно отключить, если проблемы с API
    
    def get_text(self, difficulty, force_new=False):
        """Получить текст"""
        
        # Если принудительная генерация - сразу в API
        if force_new:
            result = self._generate_via_api(difficulty)
            if result:
                cached = GeneratedTextCache.objects.create(
                    text=result['text'],
                    questions=result['questions'],
                    difficulty=difficulty,
                    used_count=0
                )
                result['id'] = cached.id
                result['source'] = 'api'
                return result
            else:
                # Если API не ответил, берём статику
                static = random.choice(self.STATIC_TEXTS.get(difficulty, self.STATIC_TEXTS[1]))
                static['source'] = 'static (fallback)'
                return static
        
        # Ищем неиспользованный текст в кэше
        cached = GeneratedTextCache.objects.filter(
            difficulty=difficulty,
            used_count=0
        ).order_by('?').first()
        
        if cached:
            return {
                'text': cached.text,
                'questions': cached.questions,
                'id': cached.id,
                'source': 'cache'
            }
        
        # Генерируем новый через API
        result = self._generate_via_api(difficulty)
        if result:
            cached = GeneratedTextCache.objects.create(
                text=result['text'],
                questions=result['questions'],
                difficulty=difficulty,
                used_count=0
            )
            result['id'] = cached.id
            result['source'] = 'api'
            return result
        
        # Fallback на статику
        static = random.choice(self.STATIC_TEXTS.get(difficulty, self.STATIC_TEXTS[1]))
        static['source'] = 'static (fallback)'
        return static
    
    def mark_as_used(self, text_id):
        """Отметить текст как использованный (удалить из кэша)"""
        if text_id:
            try:
                GeneratedTextCache.objects.filter(id=text_id).delete()
                print(f"DEBUG: Текст {text_id} удалён из кэша")
            except Exception as e:
                print(f"DEBUG: Ошибка удаления текста: {e}")
    
    def _generate_via_api(self, difficulty):
        """Генерация через API"""
        try:
            difficulty_text = {1: 'простой', 2: 'средний', 3: 'сложный'}[difficulty]
            
            prompt = f"""Создай короткий познавательный текст на русском языке {difficulty_text} уровня (5-7 предложений). Тема: любой интересный факт из истории, науки или природы.

Ответь ТОЛЬКО JSON форматом, без лишнего текста. Убедись, что JSON валидный и содержит все кавычки:
{{
    "text": "текст здесь",
    "questions": [
        {{"question": "вопрос 1 по тексту?", "answer": "ответ 1"}},
        {{"question": "вопрос 2 по тексту?", "answer": "ответ 2"}}
    ]
}}"""
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "openrouter/free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"API ошибка: статус {response.status_code}")
                return None
            
            result = response.json()
            
            # Проверяем, что ответ содержит нужные поля
            if not result.get('choices') or len(result['choices']) == 0:
                print("API ошибка: нет choices в ответе")
                return None
            
            content = result['choices'][0].get('message', {}).get('content', '')
            
            if not content or not content.strip():
                print("API ошибка: пустой content")
                return None
            
            content = content.strip()
            
            # Очищаем ответ от маркеров кода
            if '```json' in content:
                parts = content.split('```json')
                if len(parts) > 1:
                    content = parts[1].split('```')[0]
            elif '```' in content:
                parts = content.split('```')
                if len(parts) > 1:
                    content = parts[1].split('```')[0]
            
            content = content.strip()
            
            # Проверяем, что строка начинается с { и заканчивается на }
            if not content.startswith('{') or not content.endswith('}'):
                print(f"API ошибка: невалидный JSON формат. Начало: {content[:100]}")
                return None
            
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError as e:
                print(f"API ошибка: JSONDecodeError - {e}")
                print(f"Проблемный контент: {content[:200]}")
                return None
            
            # Проверяем, что есть нужные поля
            if not parsed.get('text') or not parsed.get('questions'):
                print("API ошибка: отсутствуют поля text или questions")
                return None
            
            if len(parsed['questions']) < 2:
                print("API ошибка: недостаточно вопросов")
                return None
            
            return {
                'text': parsed['text'],
                'questions': parsed['questions'][:2]
            }
            
        except requests.exceptions.Timeout:
            print("API ошибка: таймаут")
            return None
        except Exception as e:
            print(f"API ошибка: {e}")
            return None


# Создаём экземпляр для использования
generator = HybridTextGenerator()