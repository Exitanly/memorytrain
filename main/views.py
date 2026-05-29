from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from users.models import User
from tasks.models import ExerciseSession

def home(request):
    context = {}
    if request.user.is_authenticated:
        # Рассчитываем прогресс до следующего уровня
        context['progress_percent'] = request.user.get_exp_progress()
        context['exp_display'] = request.user.get_exp_current_display()
    return render(request, 'main/home.html', context)


@login_required
def rating(request):
    """Рейтинг игроков"""
    # Получаем пользователей с количеством выполненных заданий
    users = User.objects.annotate(
        completed_count=Count('exercisesession', filter=Q(exercisesession__is_completed=True))
    ).order_by('-total_points')[:10]
    
    user_data = []
    for user in users:
        user_data.append({
            'username': user.username,
            'level': user.level,
            'total_points': user.total_points,
            'completed_tasks': user.completed_count,
        })
    
    return render(request, 'main/rating.html', {'users': user_data})