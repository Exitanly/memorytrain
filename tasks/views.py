from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, UserProgress
from users.models import User

@login_required
def tasks_list(request):
    # Получаем все задания
    all_tasks = Task.objects.all().order_by('difficulty', 'category')
    
    # Получаем ID заданий, которые пользователь уже выполнил
    completed_tasks_ids = UserProgress.objects.filter(
        user=request.user, 
        completed=True
    ).values_list('task_id', flat=True)
    
    # Добавляем флаг выполнения к каждому заданию
    tasks_with_status = []
    for task in all_tasks:
        tasks_with_status.append({
            'task': task,
            'completed': task.id in completed_tasks_ids,
            'locked': task.difficulty > request.user.level  # Задания выше уровня заблокированы
        })
    
    # Группируем по категориям
    categories = {}
    for item in tasks_with_status:
        category_name = item['task'].category.name
        if category_name not in categories:
            categories[category_name] = []
        categories[category_name].append(item)
    
    context = {
        'categories': categories,
    }
    return render(request, 'tasks/list.html', context)

@login_required
def task_detail(request, task_id):
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    
    task = get_object_or_404(Task, id=task_id)
    
    # Проверка уровня
    if task.difficulty > request.user.level:
        messages.error(request, 'Это задание выше вашего уровня!')
        return redirect('tasks_list')
    
    # Проверка, не выполнено ли уже задание
    existing_progress = UserProgress.objects.filter(user=request.user, task=task, completed=True).first()
    if existing_progress:
        messages.warning(request, 'Вы уже выполнили это задание!')
        return redirect('tasks_list')
    
    # Получаем или создаем запись о прогрессе
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        task=task,
        defaults={'attempts': 1}
    )
    
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        
        progress.completed = True
        progress.score = score
        progress.save()
        
        # Начисляем опыт пользователю
        level_up = request.user.add_experience(score)
        request.user.save()
        
        if level_up:
            messages.success(request, f'Поздравляем! Вы получили {score} очков и повысили уровень до {request.user.level}!')
        else:
            messages.success(request, f'Отлично! Вы получили {score} очков!')
        
        return redirect('tasks_list')
    
    # Используем специальный шаблон для игр
    return render(request, 'tasks/game_template.html', {
        'task': task,
        'progress': progress,
    })