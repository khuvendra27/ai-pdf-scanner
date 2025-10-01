# summarize/urls.py
from django.urls import path
from .views import SummarizePDFView

urlpatterns = [
    path('summarize/', SummarizePDFView.as_view(), name='summarize_pdf'),
]
