from django.urls import path
from .views import home, upload_pdf, upload_excel, select_json, run_similarity_search, list_json_files, display_json_file

urlpatterns = [
    path('', home, name='home'),
    path('upload-pdf/', upload_pdf, name='upload_pdf'),
    path('upload-excel/', upload_excel, name='upload_excel'),
    path('select-json/', select_json, name='select_json'),
    path('run-similarity-search/<int:json1>/<int:json2>/', run_similarity_search, name='run_similarity_search'),
    path('list-json-files/', list_json_files, name='list_json_files'),
    path('display-json-file/<path:filename>/', display_json_file, name='display_json_file'),
]
