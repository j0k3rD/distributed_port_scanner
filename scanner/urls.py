from django.urls import path
from .views import ScanView, ScanListView, UpdateWorkersView

urlpatterns = [
    path('list', ScanListView.as_view(), name='scan_list'),
    path('start', ScanView.as_view(), name='scan_start'),   
    path('update_workers', UpdateWorkersView.as_view(), name='update_workers')

]