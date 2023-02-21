from django.shortcuts import render, redirect
from django.views import View

from .models import Scan
from .tasks import scan_task


class ScanView(View):
    def get(self, request):
        """Show a form to start a calculation"""
        return render(request, 'fib/start.html')

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

        return redirect('fibonacci_list')


class ScanListView(View):
    def get(self, request):
        """Show a list of past calculations"""
        context = {'executions': Scan.objects.all()}
        return render(request, 'fib/list.html', context=context)