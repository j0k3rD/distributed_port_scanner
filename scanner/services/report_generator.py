import os
from django.http import HttpResponse
from django.shortcuts import render
from models import Scan

def download_scan_results(request, task_id):
    # Buscar el escaneo completado correspondiente a la tarea con el ID dado
    try:
        Scan = Scan.objects.get(id=task_id, status='completed')
    except Scan.DoesNotExist:
        return HttpResponse('No se encontró la tarea especificada o no ha sido completada.', status=404)
    
    # Generar el archivo de texto correspondiente
    filename = f'scan_result_{task_id}.txt'
    filepath = f'/tmp/{filename}' # puede cambiar la ubicación temporal si lo desea
    with open(filepath, 'w') as f:
        f.write('Resultado del escaneo:\n\n')
        f.write(f'IP escaneada: {Scan.ip}\n')
        f.write(f'Puerto escaneada: {Scan.port}\n')
        f.write(f'Tipo de escaneo: {Scan.scanner_type}\n')
        f.write(f'Fecha de inicio: {Scan.created_at}\n')
        f.write(f'Fecha de finalización: {Scan.modified_at}\n')
        f.write('Resultados:\n')
        f.write(Scan.result)
    
    # Agregar el nombre del archivo generado al diccionario de descarga
    download_dict = {task_id: filename}
    
    # Renderizar la plantilla y enviar el diccionario de descarga
    context = {'task': Scan, 'download_dict': download_dict}
    return render(request, 'download_scan_results.html', context)
