from django.shortcuts import render, redirect
from django.views import View

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
        pending_scans = Scan.objects.filter(status=Scan.STATUS_PENDING).order_by('-id')[:3]
        error_scans = Scan.objects.filter(status=Scan.STATUS_ERROR).order_by('-id')[:3]
        success_scans = Scan.objects.filter(status=Scan.STATUS_SUCCESS).order_by('-id')[:3]
        context = {
            'pending_scans': pending_scans,
            'error_scans': error_scans,
            'success_scans': success_scans,
        }
        return render(request, 'scan/list.html', context=context)

