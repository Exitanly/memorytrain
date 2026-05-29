from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Проверка паролей
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'users/register.html')
        
        # Проверка существования пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'users/register.html')
        
        # Проверка email
        if email:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует')
                return render(request, 'users/register.html')
        else:
            messages.error(request, 'Email обязателен для восстановления пароля')
            return render(request, 'users/register.html')
        
        # Создание пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Автоматический вход после регистрации
        login(request, user)
        messages.success(request, f'Добро пожаловать, {username}! Email указан, вы сможете восстановить пароль в случае необходимости.')
        return redirect('home')
    
    return render(request, 'users/register.html')


def custom_password_reset_confirm(request, uidb64, token):
    """Собственное представление для сброса пароля"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Пароль успешно изменён! Теперь вы можете войти.')
                return redirect('users:login')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        else:
            form = SetPasswordForm(user)
    else:
        validlink = False
        form = None
    
    return render(request, 'users/password_reset_confirm.html', {
        'form': form,
        'validlink': validlink,
    })