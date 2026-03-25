from rest_framework import serializers
from .models import Company, Contact

class CompanySerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    contact_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'industry', 'country', 'logo', 'logo_url',
            'contact_count', 'created_at', 'updated_at', 'is_deleted'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None
    
    def get_contact_count(self, obj):
        return obj.contacts.filter(is_deleted=False).count()

class ContactSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Contact
        fields = [
            'id', 'full_name', 'email', 'phone', 'role', 'company',
            'company_name', 'created_at', 'updated_at', 'is_deleted'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        # Email uniqueness validation per company
        company_id = self.initial_data.get('company')
        if company_id and Contact.objects.filter(
            email=value,
            company_id=company_id,
            is_deleted=False
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Email already exists for this company")
        return value