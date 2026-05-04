from django.contrib import admin
from .models import TaskCategory, Task, UserProgress, ExerciseType, ExerciseSession, GeneratedTextCache

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

@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'generator_class', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')


@admin.register(ExerciseSession)
class ExerciseSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise_type', 'score', 'is_completed', 'started_at')
    list_filter = ('exercise_type', 'is_completed')
    search_fields = ('user__username',)
    readonly_fields = ('started_at',)


@admin.register(GeneratedTextCache)
class GeneratedTextCacheAdmin(admin.ModelAdmin):
    list_display = ('difficulty', 'used_count', 'created_at')
    list_filter = ('difficulty',)
    readonly_fields = ('created_at',)