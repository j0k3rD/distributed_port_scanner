from django.shortcuts import render
from django.http import JsonResponse
from .models import Group, Scan
from celery import current_app
from .services.functions import get_hostname
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


def index(request, group_name):
    group, _ = Group.objects.get_or_create(name=group_name)

    hostname = get_hostname()
    num_workers = current_app.control.inspect().stats()['celery@'+hostname]['pool']['max-concurrency']

    # Obtén una lista de escaneos actualizada
    pending_scans = Scan.objects.filter(status=Scan.STATUS_PENDING).order_by('-id')
    error_scans = Scan.objects.filter(status=Scan.STATUS_ERROR).order_by('-id')[:3]
    success_scans = Scan.objects.filter(status=Scan.STATUS_SUCCESS).order_by('-id')[:4]

    context = {
        'pending_scans': pending_scans,
        'error_scans': error_scans,
        'success_scans': success_scans,
        'group_name': group_name,
        'num_workers': num_workers
    }
    
    return render(request, 'scan.html', context=context)


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