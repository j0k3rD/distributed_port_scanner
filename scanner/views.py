from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from subprocess import call

from .models import Scan
from .tasks import scan_task


class ScanView(View):
    def get(self, request):
        """Show a form to start a calculation"""
        return render(request, 'scan/start.html')

    def post(self, request):
        """Process a form & start a Scan"""
        ip = request.POST['ip']
        port = request.POST['port']
        scanner_type = request.POST['scanner_type']
        scan = Scan.objects.create(
            execution=Scan.EXECUTIONS,
            scanner_type=scanner_type,
            ip=ip,
            port=port,
            status=Scan.STATUS_PENDING,
        )
        scan_task.delay(scan.id)

        return redirect('scan_list')


class ScanListView(View):
    def get(self, request):
        """Show a list of past calculations"""
        pending_scans = Scan.objects.filter(status=Scan.STATUS_PENDING).order_by('-id')
        error_scans = Scan.objects.filter(status=Scan.STATUS_ERROR).order_by('-id')[:3]
        success_scans = Scan.objects.filter(status=Scan.STATUS_SUCCESS).order_by('-id')[:4]

        current_workers = current_app.control.inspect().active().get('celery@worker1.example.com', {}).get('pool', {}).get('max-concurrency')

        context = {
            'pending_scans': pending_scans,
            'error_scans': error_scans,
            'success_scans': success_scans,
            'current_workers': current_workers,
        }
        return render(request, 'scan/list.html', context=context)



from django.contrib import messages

from celery import current_app


import os
import subprocess

class UpdateWorkersView(View):
    def get(self, request):
        current_workers = current_app.control.inspect().active().get('celery@worker1.example.com', {}).get('pool', {}).get('max-concurrency')
        return render(request, 'scan/list.html', {'current_workers': current_workers})

    def post(self, request):
        workers = request.POST.get('workers')
        try:
            workers = int(workers)
        except ValueError:
            messages.error(request, 'Debe ingresar un número válido')
            return redirect('scan_list')

        current_app.control.broadcast(
            'pool_grow', arguments={'n': workers}, destination=['celery@worker1.example.com']
        )
        
        # cambiar la variable de ambiente CELERY_WORKER_CONCURRENCY
        os.environ['CELERY_WORKER_CONCURRENCY'] = str(workers)
        
        # reiniciar celery
        subprocess.Popen(["systemctl", "restart", "celery.service"])

        messages.success(request, f'Se han agregado {workers} workers')
        return redirect('scan_list')


