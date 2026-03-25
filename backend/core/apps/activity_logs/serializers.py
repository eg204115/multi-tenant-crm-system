from rest_framework import serializers
from .models import ActivityLog
from apps.authentication.serializers import UserSerializer

class ActivityLogSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'username', 'user_details', 'action', 
            'model_name', 'object_id', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']