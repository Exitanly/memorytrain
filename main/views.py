from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    context = {}
    if request.user.is_authenticated:
        required_exp = request.user.level * 100
        progress_percent = (request.user.experience / required_exp) * 100 if required_exp > 0 else 0
        context['progress_percent'] = progress_percent
    return render(request, 'main/home.html', context)

@login_required
def rating(request):
    from users.models import User
    users = User.objects.all().order_by('-total_points')[:10]
    return render(request, 'main/rating.html', {'users': users})