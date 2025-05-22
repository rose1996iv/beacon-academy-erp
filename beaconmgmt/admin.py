from django.contrib import admin
from .models import AuditLog, BackgroundJob


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_time', 'model_name', 'action', 'model_id')
    list_filter = ('action', 'model_name', 'user')
    search_fields = ('user__username', 'model_name')
    readonly_fields = ('user', 'action_time', 'model_name', 'action', 'model_id', 'changes')


@admin.register(BackgroundJob)
class BackgroundJobAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'started_at', 'completed_at', 'user')
    list_filter = ('status', 'user')
    search_fields = ('name', 'user__username')
    readonly_fields = ('started_at', 'completed_at')
