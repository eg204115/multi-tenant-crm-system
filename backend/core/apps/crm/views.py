from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Contact
from .serializers import CompanySerializer, ContactSerializer
from core.permissions import IsManagerOrAdmin, CanDelete
from apps.activity_logs.utils import log_activity
from rest_framework.permissions import IsAuthenticated

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin, CanDelete]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'industry', 'country']
    filterset_fields = ['industry', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Company.objects.filter(
            organization=self.request.user.organization,
            is_deleted=False
        )
    
    def perform_create(self, serializer):
        company = serializer.save(organization=self.request.user.organization)
        log_activity(
            user=self.request.user,
            action='CREATE',
            model_name='Company',
            object_id=company.id,
            organization=self.request.user.organization
        )
    
    def perform_update(self, serializer):
        company = serializer.save()
        log_activity(
            user=self.request.user,
            action='UPDATE',
            model_name='Company',
            object_id=company.id,
            organization=self.request.user.organization
        )
    
    def perform_destroy(self, instance):
        log_activity(
            user=self.request.user,
            action='DELETE',
            model_name='Company',
            object_id=instance.id,
            organization=self.request.user.organization
        )
        instance.soft_delete()
    
    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        company = self.get_object()
        contacts = company.contacts.filter(is_deleted=False)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin, CanDelete]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'role']
    filterset_fields = ['company', 'role']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Contact.objects.filter(
            organization=self.request.user.organization,
            is_deleted=False
        )
    
    def perform_create(self, serializer):
        contact = serializer.save(organization=self.request.user.organization)
        log_activity(
            user=self.request.user,
            action='CREATE',
            model_name='Contact',
            object_id=contact.id,
            organization=self.request.user.organization
        )
    
    def perform_update(self, serializer):
        contact = serializer.save()
        log_activity(
            user=self.request.user,
            action='UPDATE',
            model_name='Contact',
            object_id=contact.id,
            organization=self.request.user.organization
        )
    
    def perform_destroy(self, instance):
        log_activity(
            user=self.request.user,
            action='DELETE',
            model_name='Contact',
            object_id=instance.id,
            organization=self.request.user.organization
        )
        instance.soft_delete()