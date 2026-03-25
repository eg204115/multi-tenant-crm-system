from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Organization
from .serializers import OrganizationSerializer
from core.permissions import IsAdmin

class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        # Admin can see all organizations, others only their own
        if self.request.user.role == 'admin':
            return Organization.objects.all()
        return Organization.objects.filter(id=self.request.user.organization.id)
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        organization = self.get_object()
        users = organization.users.all()
        from apps.authentication.serializers import UserSerializer
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)