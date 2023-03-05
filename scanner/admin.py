from django.contrib import admin
from .models import Scan, Group

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ['id', 'execution', 'ipv_type', 'scanner_type', 'ip', 'port', 'result', 'created_at', 'modified_at', 'status', 'message', 'group']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']