from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'users/register.html')
        
        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        login(request, user)
        messages.success(request, f'Добро пожаловать, {username}!')
        return redirect('home')
    
    return render(request, 'users/register.html')