from django.urls import path
from .views import home, upload_pdf, query_view

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_pdf, name='upload_pdf'),
    path('query/', query_view, name='query_view'),
]
