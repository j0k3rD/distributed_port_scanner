from django.urls import path
from .views import ScanView, ScanListView, DownloadScanResultsView, DownloadAllScanResultsView

urlpatterns = [
    path('start/', ScanView.as_view(), name='scan_start'),
    path('list/', ScanListView.as_view(), name='scan_list'),
    path('download/<int:scan_id>/', DownloadScanResultsView.as_view(), name='download_scan_results'),
    path('download/all/', DownloadAllScanResultsView.as_view(), name='download_all_scan_results'),
]