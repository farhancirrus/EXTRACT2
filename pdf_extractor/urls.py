import json
import os
from django_distill import distill_path
from .views import home, upload_pdf, upload_excel, select_json, run_similarity_search, list_json_files, display_json_file
from django.conf import settings
from django.core.paginator import Paginator

def get_all_pages():
    # Get all JSON files from the project root
    json_files = [f for f in os.listdir(settings.BASE_DIR) if f.endswith('.json')]
    
    for filename in json_files:
        file_path = os.path.join(settings.BASE_DIR, filename)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        
        # Create a paginator object
        paginator = Paginator(json_data, 10)  # Assuming 10 items per page
        
        # Generate URLs for each page
        for page_num in range(1, paginator.num_pages + 1):
            yield {
                'filename': filename,
                'page': page_num
            }

def get_similarity_search_urls():
    json_files = [f for f in os.listdir(settings.BASE_DIR) if f.endswith('.json')]
    for i, json1 in enumerate(json_files):
        for json2 in json_files[i+1:]:  # This avoids duplicate combinations
            yield {'json1': json1, 'json2': json2}

urlpatterns = [
    distill_path('', home, name='home'),
    distill_path('upload-pdf/', upload_pdf, name='upload_pdf'),
    distill_path('upload-excel/', upload_excel, name='upload_excel'),
    distill_path('select-json/', select_json, name='select_json'),
    distill_path('run-similarity-search/<int:json1>/<int:json2>/', run_similarity_search, name='run_similarity_search', distill_func=get_similarity_search_urls),
    distill_path('list-json-files/', list_json_files, name='list_json_files'),
    distill_path('display-json-file/<path:filename>/', display_json_file, name='display_json_file', distill_func=get_all_pages),
]
