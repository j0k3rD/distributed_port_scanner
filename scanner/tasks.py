import requests
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Scan
from .services.port_scanning_ipv4 import *
from .services.port_scanning_ipv6 import *


channel_layer = get_channel_layer()


@shared_task
def scan_task(scan_id):
    try:
        execution = Scan.objects.get(id=scan_id)
        scan_type = execution.scanner_type
        ipv_type = execution.ipv_type
        ip = execution.ip
        port = execution.port
        
        if ipv_type == 'ipv4': 
            if scan_type == 'python':
                scan_result = scan_with_python_ipv4(ip, port)
            elif scan_type == 'nmap':
                scan_result = scan_with_nmap_ipv4(ip, port)
            if execution.port == '':
                execution.port = '0-65535'
            execution.result = scan_result
            execution.status = Scan.STATUS_SUCCESS
        elif ipv_type == 'ipv6':
            if scan_type == 'python':
                scan_result = scan_with_python_ipv6(ip, port)
            elif scan_type == 'nmap':
                scan_result = scan_with_nmap_ipv6(ip, port)
            if execution.port == '':
                execution.port = '0-65535'
            execution.result = scan_result
            execution.status = Scan.STATUS_SUCCESS

        execution.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "scanner",
            {
                "type": "send_scan",
                "text": execution.id
            }
        )
    except Exception as e:
        execution.status = Scan.STATUS_ERROR
        execution.message = str(e)[:110]
        execution.save()