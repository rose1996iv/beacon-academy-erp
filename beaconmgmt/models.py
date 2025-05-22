from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    """
    A model to track changes to data in the system.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_time = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=[
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ])
    model_id = models.IntegerField()
    changes = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-action_time']

    def __str__(self):
        return f"{self.user} - {self.action} {self.model_name} at {self.action_time}"


class BackgroundJob(models.Model):
    """
    A model to track background jobs like report generation or data imports.
    """
    name = models.CharField(max_length=100)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ], default='PENDING')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    error_message = models.TextField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.name} - {self.status} ({self.started_at})"
