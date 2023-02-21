from django.urls import path
from .views import ScanView, ScanListView

urlpatterns = [
    path('list', ScanListView.as_view(), name='fibonacci_list'),
    path('start', ScanView.as_view(), name='fibonacci_start'),
]