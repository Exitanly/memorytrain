from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from .models import ExerciseType, ExerciseSession
from .generators import GENERATORS
import json

@login_required
def exercise_list(request):
    """Страница со списком категорий и упражнений"""
    exercises = ExerciseType.objects.filter(is_active=True).order_by('category', 'order')
    
    categories = {
        'visual': {'name': 'Визуальная память', 'exercises': []},
        'number': {'name': 'Числовая память', 'exercises': []},
        'text': {'name': 'Текстовая память', 'exercises': []},
    }
    
    for ex in exercises:
        categories[ex.category]['exercises'].append(ex)
    
    return render(request, 'tasks_new/exercise_list.html', {'categories': categories})


@login_required
def exercise_play(request, slug):
    """Страница выполнения упражнения"""
    exercise_type = get_object_or_404(ExerciseType, slug=slug, is_active=True)
    
    # Определяем сложность на основе уровня пользователя
    if request.user.level <= 3:
        difficulty = 1
    elif request.user.level <= 7:
        difficulty = 2
    else:
        difficulty = 3
    
    # Получаем класс генератора
    generator_class = GENERATORS.get(exercise_type.generator_class)
    if not generator_class:
        messages.error(request, 'Упражнение временно недоступно')
        return redirect('exercise_list')
    
    # Генерируем задание
    generator = generator_class(difficulty)
    task = generator.generate()
    
    # Сохраняем данные проверки в сессию
    request.session['current_exercise'] = {
        'slug': slug,
        'generator_class': exercise_type.generator_class,
        'difficulty': difficulty,
        'check_data': task['check_data'],
        'max_time': task['max_time'],
    }
    
    context = {
        'exercise': exercise_type,
        'difficulty': difficulty,
        'task_data': task['task_data'],
        'max_time': task['max_time'],
    }
    
    # Пытаемся найти шаблон для конкретного упражнения
    template_name = f'tasks_new/games/{slug}.html'
    try:
        get_template(template_name)
        return render(request, template_name, context)
    except TemplateDoesNotExist:
        return render(request, 'tasks_new/game_base.html', context)


@login_required
def exercise_check(request, slug):
    """Проверка ответа"""
    print(f"\n=== DEBUG: Проверка упражнения {slug} ===")
    
    if request.method != 'POST':
        print("DEBUG: Не POST запрос")
        return redirect('exercise_list')
    
    exercise_type = get_object_or_404(ExerciseType, slug=slug)
    
    session_data = request.session.get('current_exercise')
    print(f"DEBUG: session_data = {session_data}")
    
    if not session_data or session_data.get('slug') != slug:
        messages.error(request, 'Сессия истекла. Начните заново.')
        return redirect('exercise_play', slug=slug)
    
    user_answer = request.POST.get('answer')
    print(f"DEBUG: Получен ответ (raw): {user_answer}")
    print(f"DEBUG: Тип ответа: {type(user_answer)}")
    
    if not user_answer:
        messages.error(request, 'Пожалуйста, дайте ответ')
        return redirect('exercise_play', slug=slug)
    
    # Парсим ответ
    parsed_answer = user_answer
    try:
        if user_answer.startswith('{'):
            parsed_answer = json.loads(user_answer)
            print(f"DEBUG: Распарсили в JSON: {parsed_answer}")
    except Exception as e:
        print(f"DEBUG: Ошибка парсинга JSON: {e}")
    
    # Получаем генератор
    generator_class = GENERATORS.get(session_data['generator_class'])
    print(f"DEBUG: generator_class = {generator_class}")
    
    generator = generator_class(session_data['difficulty'])
    
    # Проверяем ответ
    is_correct, message = generator.check_answer(parsed_answer, session_data['check_data'])
    print(f"DEBUG: is_correct = {is_correct}")
    print(f"DEBUG: message = {message}")
    
    # Рассчитываем очки
    score = generator.calculate_score(is_correct, 10, 1) if is_correct else 0
    print(f"DEBUG: score = {score}")
    
    # Сохраняем сессию
    ExerciseSession.objects.create(
        user=request.user,
        exercise_type=exercise_type,
        score=score,
        is_completed=True,
        details={
            'difficulty': session_data['difficulty'],
            'is_correct': is_correct,
            'score': score,
            'user_answer': str(user_answer),
        }
    )
    
    # Начисляем опыт
    if score > 0:
        level_up = request.user.add_experience(score)
        request.user.save()
        if level_up:
            messages.success(request, f'Поздравляем! Вы получили {score} очков и повысили уровень до {request.user.level}!')
        else:
            messages.success(request, f'Отлично! Вы получили {score} очков!')
    else:
        messages.warning(request, message)
    
    # Очищаем сессию
    if 'current_exercise' in request.session:
        del request.session['current_exercise']
    
    print("=== DEBUG: Конец проверки ===\n")
    
    return redirect('exercise_play', slug=slug)