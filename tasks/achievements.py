from django.db.models import Q
from .models import Achievement, UserAchievement, ExerciseSession

class AchievementChecker:
    """Проверка и выдача достижений"""
    
    @staticmethod
    def check_all_achievements(user, event_type=None, event_data=None):
        """Проверяет все достижения для пользователя"""
        earned = []
        
        achievements = Achievement.objects.filter(is_active=True)
        
        for achievement in achievements:
            if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
                continue
            
            if AchievementChecker._check_condition(user, achievement, event_type, event_data):
                UserAchievement.objects.create(user=user, achievement=achievement)
                if achievement.reward_points > 0:
                    user.add_experience(achievement.reward_points)
                earned.append(achievement)
        
        return earned
    
    @staticmethod
    def _check_condition(user, achievement, event_type, event_data):
        """Проверка конкретного условия"""
        
        condition_type = achievement.condition_type
        value = achievement.condition_value
        
        if condition_type == 'tasks_completed':
            # Количество выполненных заданий
            count = ExerciseSession.objects.filter(user=user, is_completed=True).count()
            return count >= value
        
        elif condition_type == 'perfect_tasks':
            # Количество заданий без ошибок
            perfect_count = 0
            for session in ExerciseSession.objects.filter(user=user, is_completed=True):
                details = session.details
                if isinstance(details, dict):
                    results = details.get('results', [])
                    if results and all(r is True for r in results):
                        perfect_count += 1
            return perfect_count >= value
        
        elif condition_type == 'level_reached':
            return user.level >= value
        
        elif condition_type == 'points_total':
            return user.total_points >= value
        
        elif condition_type == 'specific_task_perfect':
            slug = achievement.condition_extra
            if not slug or not event_data:
                return False
            return (event_type == 'task_completed' and 
                    event_data.get('slug') == slug and 
                    event_data.get('perfect', False))
        
        elif condition_type == 'hard_difficulty_task':
            if event_type == 'task_completed':
                return event_data.get('difficulty') == 3
        
        elif condition_type == 'specific_task_hard':
            slug = achievement.condition_extra
            if not slug:
                return False
            if event_type == 'task_completed':
                return (event_data.get('slug') == slug and 
                        event_data.get('difficulty') == 3)
        
        return False


def get_user_achievements(user):
    """Возвращает список достижений пользователя с отметкой о получении"""
    achievements = Achievement.objects.filter(is_active=True).order_by('order')
    user_achievement_ids = UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
    
    result = []
    for ach in achievements:
        earned = ach.id in user_achievement_ids
        earned_at = None
        if earned:
            ua = UserAchievement.objects.filter(user=user, achievement=ach).first()
            earned_at = ua.earned_at if ua else None
        
        result.append({
            'id': ach.id,
            'name': ach.name,
            'description': ach.description,
            'icon': ach.icon,
            'reward_points': ach.reward_points,
            'earned': earned,
            'earned_at': earned_at,
        })
    return result


def get_achievement_stats(user):
    """Возвращает статистику достижений"""
    achievements = Achievement.objects.filter(is_active=True)
    earned_count = UserAchievement.objects.filter(user=user).count()
    total_count = achievements.count()
    progress = int(earned_count / total_count * 100) if total_count > 0 else 0
    return {
        'earned': earned_count,
        'total': total_count,
        'progress': progress,
    }