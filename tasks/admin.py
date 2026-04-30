from django.contrib import admin
from .models import TaskCategory, Task, UserProgress

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'task_type', 'difficulty', 'base_points')
    list_filter = ('difficulty', 'task_type', 'category')
    search_fields = ('title', 'description')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'completed', 'score', 'completed_at')
    list_filter = ('completed', 'user')