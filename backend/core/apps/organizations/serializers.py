from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = ['id', 'name', 'subscription_plan', 'created_at', 'user_count']
        read_only_fields = ['id', 'created_at']
    
    def get_user_count(self, obj):
        return obj.users.count()