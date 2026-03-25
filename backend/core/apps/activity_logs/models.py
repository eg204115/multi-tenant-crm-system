from django.db import models

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='activities')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.model_name} - {self.object_id} at {self.timestamp}"