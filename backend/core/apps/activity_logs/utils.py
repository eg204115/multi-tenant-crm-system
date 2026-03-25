from .models import ActivityLog

def log_activity(user, action, model_name, object_id, organization):
    """Helper function to log activities"""
    ActivityLog.objects.create(
        user=user,
        organization=organization,
        action=action,
        model_name=model_name,
        object_id=object_id
    )