from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),
    path('<int:task_id>/', views.task_detail, name="task_detail"),
]