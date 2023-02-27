from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from subprocess import call
from django.http import HttpResponse
from django.contrib import messages
import os
import subprocess
from .models import Scan
from .tasks import scan_task
from celery import current_app
from django.shortcuts import get_object_or_404
import shlex
import psutil
from subprocess import Popen, PIPE

def get_hostname():
    hostname = Popen(['hostname'], stdout=PIPE).communicate()[0]
    return hostname.decode('utf-8').strip()

class ScanView(View):
    def get(self, request):
        """Show a form to start a calculation"""
        return render(request, 'scan/start.html')

    def post(self, request):
        """Process a form & start a Scan"""
        ip = request.POST['ip']
        port = request.POST['port']
        ipv_type = request.POST['ipv_type']
        scanner_type = request.POST['scanner_type']
        scan = Scan.objects.create(
            execution=Scan.EXECUTIONS,
            ipv_type=ipv_type,
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

        hostname = get_hostname()
        num_workers = current_app.control.inspect().stats()['celery@'+hostname]['pool']['max-concurrency']

        context = {
            'pending_scans': pending_scans,
            'error_scans': error_scans,
            'success_scans': success_scans,
            'num_workers': num_workers,
        }
        return render(request, 'scan/list.html', context=context)


class DownloadScanResultsView(View):
    def get(self, request, scan_id):
        # Buscar el escaneo completado correspondiente a la tarea con el ID dado
        scan = get_object_or_404(Scan, id=scan_id, status=Scan.STATUS_SUCCESS)

        # Generar el archivo de texto correspondiente
        filename = f'scan_result_{scan_id}.txt'
        filepath = f'/tmp/{filename}' # puede cambiar la ubicación temporal si lo desea
        with open(filepath, 'w') as f:
            f.write('Resultado del escaneo:\n\n')
            f.write(f'IP escaneada: {scan.ip}\n')
            f.write(f'Puerto escaneada: {scan.port}\n')
            f.write(f'Tipo de escaneo: {scan.scanner_type}\n')
            f.write(f'Fecha de inicio: {scan.created_at}\n')
            f.write(f'Fecha de finalización: {scan.modified_at}\n')
            f.write('Resultados:\n')
            f.write(scan.result)
            for n in range(5):
                f.write('\n')
            f.write('--Escaneo realizado por: "distributed_ports_scanner" - @j0k3rD --')
        # Crear la respuesta HTTP con el archivo de texto adjunto
        response = HttpResponse(open(filepath, 'rb'), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class DownloadAllScanResultsView(View):
    def get(self, request):
        # Obtener todos los escaneos completados
        scans = Scan.objects.filter(status=Scan.STATUS_SUCCESS)

        # Generar el archivo de texto correspondiente
        filename = 'all_scan_results.txt'
        filepath = f'/tmp/{filename}' # puede cambiar la ubicación temporal si lo desea
        with open(filepath, 'w') as f:
            f.write('Resultados de todos los escaneos realizados:\n\n')
            for scan in scans:
                f.write(f'ID del escaneo: {scan.id}\n')
                f.write(f'IP escaneada: {scan.ip}\n')
                f.write(f'Puerto escaneado: {scan.port}\n')
                f.write(f'Tipo de escaneo: {scan.scanner_type}\n')
                f.write(f'Fecha de inicio: {scan.created_at}\n')
                f.write(f'Fecha de finalización: {scan.modified_at}\n')
                f.write('Resultados:\n')
                f.write(scan.result)
                for n in range(5):
                    f.write('\n')
                f.write('--Escaneo realizado por: "distributed_ports_scanner" - @j0k3rD --')
                f.write('\n\n')

        # Crear la respuesta HTTP con el archivo de texto adjunto
        response = HttpResponse(open(filepath, 'rb'), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response