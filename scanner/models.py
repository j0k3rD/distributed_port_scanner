from django.db import models

# class Scan(models.Model):
    # content = models.CharField(max_length=1000, default='')
    # created_at = models.DateTimeField(auto_now_add=True)
    # group = models.ForeignKey('Group', on_delete=models.CASCADE, default=1)

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Scan(models.Model):
    """Track a calculation and its results"""
    EXECUTION_SCANS = 'SCAN'
    EXECUTIONS = ((EXECUTION_SCANS, 'Scan'),)

    STATUS_PENDING = 'PENDING'
    STATUS_ERROR = 'ERROR'
    STATUS_SUCCESS = 'SUCCESS'
    STATUSES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_ERROR, 'Error'),
        (STATUS_SUCCESS, 'Success'),
    )

    execution = models.CharField(max_length=8, choices=EXECUTIONS, default=EXECUTION_SCANS)
    ipv_type = models.CharField(max_length=20, blank=True, null=True)
    scanner_type = models.CharField(max_length=20, default='')
    ip = models.GenericIPAddressField(default='')
    port = models.CharField(max_length=9, default='')
    result = models.CharField(blank=True, null=True, max_length=400)

    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, choices=STATUSES, default=STATUS_PENDING)
    message = models.CharField(max_length=110, blank=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, default=1)