from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from .models import ExerciseType, ExerciseSession, GeneratedTextCache
from .generators import GENERATORS
import json
from .achievements import AchievementChecker
@login_required
def exercise_list(request):
    """Страница со списком категорий и упражнений"""
    # Получаем выбранную сложность из GET параметра или сессии
    selected_difficulty = request.GET.get('difficulty')
    if selected_difficulty:
        selected_difficulty = int(selected_difficulty)
        # Проверяем, может ли пользователь выбрать эту сложность
        if request.user.can_access_difficulty(selected_difficulty):
            request.session['selected_difficulty'] = selected_difficulty
        else:
            messages.warning(request, f'Эта сложность недоступна. Нужен уровень {5 if selected_difficulty == 2 else 10}')
            selected_difficulty = request.session.get('selected_difficulty', 1)
    else:
        selected_difficulty = request.session.get('selected_difficulty', 1)
    
    # Убеждаемся, что выбранная сложность доступна
    if not request.user.can_access_difficulty(selected_difficulty):
        selected_difficulty = 1
        request.session['selected_difficulty'] = 1
    
    # Получаем упражнения
    exercises = ExerciseType.objects.filter(is_active=True).order_by('category', 'order')
    
    categories = {
        'visual': {'name': 'Визуальная память', 'exercises': []},
        'number': {'name': 'Числовая память', 'exercises': []},
        'text': {'name': 'Текстовая память', 'exercises': []},
    }
    
    for ex in exercises:
        categories[ex.category]['exercises'].append(ex)
    
    # Подготавливаем данные о доступности сложностей для шаблона
    context = {
        'categories': categories,
        'current_difficulty': selected_difficulty,
        'can_medium': request.user.can_access_difficulty(2),
        'can_hard': request.user.can_access_difficulty(3),
    }
    
    return render(request, 'tasks_new/exercise_list.html', context)


@login_required
def exercise_play(request, slug):
    """Страница выполнения упражнения"""
    exercise_type = get_object_or_404(ExerciseType, slug=slug, is_active=True)
    
    # Получаем выбранную сложность (из GET или сессии)
    url_difficulty = request.GET.get('difficulty')
    if url_difficulty:
        difficulty = int(url_difficulty)
    else:
        difficulty = request.session.get('selected_difficulty', 1)
    
    # Проверяем, может ли пользователь играть на этой сложности
    if not request.user.can_access_difficulty(difficulty):
        messages.error(request, f'Эта сложность недоступна до {5 if difficulty == 2 else 10} уровня!')
        difficulty = 1
    
    # Получаем класс генератора
    generator_class = GENERATORS.get(exercise_type.generator_class)
    if not generator_class:
        messages.error(request, 'Упражнение временно недоступно')
        return redirect('exercise_list')
    
    # Для text-questions используем отдельную логику с сохранением текста
    if slug == 'text-questions':
        # Проверяем, есть ли текст на удаление (приходим сюда после правильных ответов)
        text_to_delete = request.session.pop('text_to_delete', None)
        
        # Проверяем, нужно ли сгенерировать новый текст
        generate_new = request.GET.get('new') == '1'
        
        # Если generate_new=True - удаляем старый текст и генерируем новый
        if generate_new and text_to_delete:
            try:
                from .services.text_generator import generator as text_gen
                text_gen.mark_as_used(text_to_delete)
                print(f"DEBUG: Текст {text_to_delete} удалён при генерации нового")
                request.session.pop('saved_text_id', None)
            except Exception as e:
                print(f"DEBUG: Ошибка удаления текста: {e}")
        
        # Проверяем, есть ли сохранённый текст в сессии
        saved_text_id = request.session.get('saved_text_id')
        
        task = None
        
        if not generate_new and saved_text_id:
            # Пытаемся восстановить текст из кэша
            try:
                cached_text = GeneratedTextCache.objects.filter(id=saved_text_id).first()
                if cached_text:
                    task = {
                        'task_data': {
                            'text': cached_text.text,
                            'questions': cached_text.questions,
                            'total_questions': len(cached_text.questions),
                            'text_id': cached_text.id,
                        },
                        'check_data': {
                            'questions': cached_text.questions,
                            'text_id': cached_text.id,
                        },
                        'max_time': 0,
                    }
            except Exception as e:
                print(f"Ошибка восстановления текста: {e}")
        
        if not task:
            # Генерируем новый текст
            generator = generator_class(difficulty)
            task = generator.generate(force_new=generate_new)
            text_id = task['task_data'].get('text_id')
            if text_id:
                request.session['saved_text_id'] = text_id
        
        # Сохраняем данные проверки в сессию
        request.session['current_exercise'] = {
            'slug': slug,
            'generator_class': exercise_type.generator_class,
            'difficulty': difficulty,
            'check_data': task['check_data'],
            'max_time': task['max_time'],
            'text_id': task['task_data'].get('text_id'),
        }
        
        context = {
            'exercise': exercise_type,
            'difficulty': difficulty,
            'task_data': task['task_data'],
            'max_time': task['max_time'],
        }
        
    else:
        # Для остальных упражнений - обычная логика
        generator = generator_class(difficulty)
        task = generator.generate()
        
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
        return redirect('exercise_list')
    
    exercise_type = get_object_or_404(ExerciseType, slug=slug)
    
    session_data = request.session.get('current_exercise')
    print(f"DEBUG: session_data = {session_data}")
    
    if not session_data or session_data.get('slug') != slug:
        messages.error(request, 'Сессия истекла. Начните заново.')
        return redirect('exercise_play', slug=slug)
    
    user_answer = request.POST.get('answer')
    print(f"DEBUG: Получен ответ (raw): {user_answer}")
    
    if not user_answer:
        messages.error(request, 'Пожалуйста, дайте ответ')
        return redirect('exercise_play', slug=slug)
    
    # Парсим ответ
    parsed_answer = user_answer
    try:
        if user_answer.startswith('{') or user_answer.startswith('['):
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
    
    # Получаем детали проверки (для text-questions)
    check_results = getattr(generator, 'check_results', {})
    text_id = session_data.get('text_id')
    
    # Рассчитываем очки
    score = generator.calculate_score(is_correct, 10, 1) if is_correct else 0
    print(f"DEBUG: score = {score}")
    
    # Сохраняем сессию выполнения
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
            'results': check_results.get('results', []),
        }
    )
    
    # Если ответ правильный - помечаем текст на удаление (но не удаляем сейчас)
    if is_correct and text_id and slug == 'text-questions':
        request.session['text_to_delete'] = text_id
        # НЕ удаляем saved_text_id из сессии, чтобы текст не генерировался заново при редиректе
        print(f"DEBUG: Текст {text_id} помечен на удаление")
    
    # Начисляем опыт
    if score > 0:
        level_up = request.user.add_experience(score)
        request.user.save()
        if level_up:
            messages.success(request, f'Поздравляем! Вы получили {score} очков и повысили уровень до {request.user.level}!')
        else:
            messages.success(request, f'Отлично! Вы получили {score} очков!')
        #  Проверяем достижения
        is_perfect = False
        if check_results.get('total', 0) > 0:
            is_perfect = check_results.get('correct_count', 0) == check_results.get('total', 0)
        
        event_data = {
            'slug': slug,
            'difficulty': session_data['difficulty'],
            'perfect': is_perfect,
            'score': score,
        }
        earned = AchievementChecker.check_all_achievements(request.user, 'task_completed', event_data)
        
        for ach in earned:
            messages.success(request, f'🏆 Получено достижение: {ach.name}! +{ach.reward_points} очков')
    else:
        messages.warning(request, message)
    
    # Очищаем сессию current_exercise
    if 'current_exercise' in request.session:
        del request.session['current_exercise']
    
    print("=== DEBUG: Конец проверки ===\n")
    
    # Перенаправляем обратно на то же упражнение с параметром результата
    return redirect(f'/tasks/exercises/{slug}/?result={"success" if is_correct else "fail"}')