from django.urls import path
from . import views

urlpatterns = [
    path('<str:group_name>/', views.index, name='index'),
    path('download/<int:scan_id>/', views.DownloadScanResultsView.as_view(), name='download_scan_results'),
    path('download/all/', views.DownloadAllScanResultsView.as_view(), name='download_all_scan_results'),
]