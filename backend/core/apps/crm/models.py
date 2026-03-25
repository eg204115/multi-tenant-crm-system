from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone

class BaseModel(models.Model):
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_set'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

class Company(BaseModel):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    logo = models.FileField(upload_to='company_logos/', null=True, blank=True)
    
    class Meta:
        db_table = 'companies'
        unique_together = ['name', 'organization']  # Company name unique per organization
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Contact(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\d{8,15}$', message='Phone must be 8-15 digits')],
        null=True,
        blank=True
    )
    role = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'contacts'
        unique_together = ['email', 'company']  # Email unique per company
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.company.name}"