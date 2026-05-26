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
    
    def get_text(self, difficulty, force_new=False):
        """Получить текст"""
        
        # Если принудительная генерация - сразу в API
        if force_new:
            result = self._generate_via_api(difficulty)
            if result:
                # Сохраняем в кэш
                cached = GeneratedTextCache.objects.create(
                    text=result['text'],
                    questions=result['questions'],
                    difficulty=difficulty,
                    used_count=0
                )
                result['id'] = cached.id
                result['source'] = 'api'
                return result
        
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
        
        # Если нет неиспользованных - генерируем новый
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
        
        # Fallback на статику (если API не работает)
        static_list = self.STATIC_TEXTS.get(difficulty, self.STATIC_TEXTS[1])
        static = random.choice(static_list)
        static['source'] = 'static'
        static['id'] = None
        return static
    
    def mark_as_used(self, text_id):
        """Отметить текст как использованный (удалить из кэша)"""
        if text_id:
            GeneratedTextCache.objects.filter(id=text_id).delete()
    
    def _generate_via_api(self, difficulty):
        """Генерация через API"""
        try:
            difficulty_text = {1: 'простой', 2: 'средний', 3: 'сложный'}[difficulty]
            
            prompt = f"""Создай короткий познавательный текст на русском языке {difficulty_text} уровня (5-7 предложений). Тема: любой интересный факт из истории, науки или природы.

Ответь ТОЛЬКО JSON форматом, без лишнего текста:
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
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                content = content.strip()
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0]
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0]
                
                parsed = json.loads(content)
                return {
                    'text': parsed['text'],
                    'questions': parsed['questions'][:2]
                }
            
            print(f"API ошибка: статус {response.status_code}")
            return None
            
        except Exception as e:
            print(f"API ошибка: {e}")
            return None


# Создаём экземпляр для использования
generator = HybridTextGenerator()