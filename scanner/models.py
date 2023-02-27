from django.db import models


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

    execution = models.CharField(max_length=8, choices=EXECUTIONS)
    ipv_type = models.CharField(max_length=20, blank=True, null=True)
    scanner_type = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    port = models.CharField(max_length=9)
    result = models.CharField(blank=True, null=True, max_length=400)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, choices=STATUSES)
    message = models.CharField(max_length=110, blank=True)


# class User(models.Model):
#     mac = models.CharField(max_length=17)
#     created_at = models.DateTimeField(auto_now_add=True)
#     scan = models.ForeignKey(Scan, on_delete=models.CASCADE, blank=True, null=True)