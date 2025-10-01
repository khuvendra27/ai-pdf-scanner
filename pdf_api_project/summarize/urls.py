# summarize/urls.py
from django.urls import path
from .views import SummarizePDFView, AuditLogsView

urlpatterns = [
    path('summarize/', SummarizePDFView.as_view(), name='summarize_pdf'),
    path('audit_logs/', AuditLogsView.as_view(), name='get_audit'),
]
