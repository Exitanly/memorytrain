from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    context = {}
    if request.user.is_authenticated:
        # Рассчитываем прогресс до следующего уровня
        context['progress_percent'] = request.user.get_exp_progress()
        context['exp_display'] = request.user.get_exp_current_display()
    return render(request, 'main/home.html', context)


@login_required
def rating(request):
    from users.models import User
    users = User.objects.all().order_by('-total_points')[:10]
    return render(request, 'main/rating.html', {'users': users})