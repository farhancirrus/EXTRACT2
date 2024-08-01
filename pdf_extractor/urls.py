from django.urls import path
from .views import home, upload_pdf, query_view, upload_excel
import logging

logger = logging.getLogger(__name__)

urlpatterns = [
    path('', home, name='home'),
    path('upload-pdf/', upload_pdf, name='upload_pdf'),
    path('upload-excel/', upload_excel, name='upload_excel'),
    path('query/', query_view, name='query_view'),
]
