from django.urls import path
from . import views_new as views

urlpatterns = [
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/<slug:slug>/', views.exercise_play, name='exercise_play'),
    path('exercises/<slug:slug>/check/', views.exercise_check, name='exercise_check'),
]