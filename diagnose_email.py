# check_email.py
import os
import django
from django.core.mail import send_mail

# Настройка окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_trainer.settings')
django.setup()

try:
    print("Попытка отправить тестовое письмо...")
    send_mail(
        'Тест отправки с Django',
        'Это тестовое письмо для проверки конфигурации SMTP Gmail.',
        None,  # Будет использовано значение DEFAULT_FROM_EMAIL
        ['exdicem@mail.ru'], # Сюда можно указать любой ваш email для получения теста
        fail_silently=False,
    )
    print("✅ Тестовое письмо успешно отправлено! Проверьте ваш почтовый ящик.")
except Exception as e:
    print(f"❌ Ошибка при отправке: {e}")