from django.db import models
from django.utils import timezone

class Organization(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    subscription_plan = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default='basic')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name