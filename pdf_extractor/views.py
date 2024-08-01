from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PDFUploadForm, ExcelUploadForm
from .models import JSONDocument
from urllib.parse import quote, unquote
import json
import logging
import pandas as pd
import os
from django.conf import settings
from extract_mvp import extract_text_from_pdf, process_text_to_json
from extract_xls import excel_to_json
from similarity_search import save_json_document, load_json, preprocess_data, initialize_chroma_collection, generate_output

logger = logging.getLogger(__name__)

JSON_FILES_DIR = os.path.join(settings.MEDIA_ROOT, 'jsons')

def home(request):
    return render(request, 'pdf_extractor/home.html')

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = form.save()
            extracted_text = extract_text_from_pdf(pdf_document.file.path, 0, 75)
            json_output = process_text_to_json(extracted_text)
            original_filename = pdf_document.file.name.rsplit('.', 1)[0]
            version = form.cleaned_data['version']
            save_json_document(json.loads(json_output), original_filename, version)
            return render(request, 'pdf_extractor/pdf_result.html', {'json_data': json.loads(json_output)})
    else:
        form = PDFUploadForm()
    return render(request, 'pdf_extractor/upload_pdf.html', {'form': form})

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_document = form.save()
                file_path = excel_document.file.path
                sheet_name = form.cleaned_data['sheet_name']
                version = form.cleaned_data['version']

                extracted_json = excel_to_json(file_path, sheet_name)
                original_filename = excel_document.file.name.rsplit('.', 1)[0]
                save_json_document(json.loads(extracted_json), original_filename, version)
                return render(request, 'pdf_extractor/excel_result.html', {'json_data': json.loads(extracted_json)})
            except Exception as e:
                logger.error(f"Error processing Excel file: {e}")
                return render(request, 'pdf_extractor/upload_excel.html', {'form': form, 'error': str(e)})
    else:
        form = ExcelUploadForm()
    return render(request, 'pdf_extractor/upload_excel.html', {'form': form})

def select_json(request):
    json_files = JSONDocument.objects.all()
    if request.method == 'POST':
        json_file_1 = request.POST.get('json_file_1')
        json_file_2 = request.POST.get('json_file_2')
        if not json_file_1 or not json_file_2:
            return render(request, 'pdf_extractor/select_json.html', {'json_files': json_files, 'error': 'Please select two JSON files.'})
        if json_file_1 == json_file_2:
            return render(request, 'pdf_extractor/select_json.html', {'json_files': json_files, 'error': 'Please select two different JSON files.'})
        return redirect('run_similarity_search', json1=json_file_1, json2=json_file_2)
    return render(request, 'pdf_extractor/select_json.html', {'json_files': json_files})

def run_similarity_search(request, json1, json2):
    json1_doc = JSONDocument.objects.get(id=json1)
    json2_doc = JSONDocument.objects.get(id=json2)

    with open(json1_doc.file.path, 'r') as file:
        adhics_v1 = json.load(file)
    
    with open(json2_doc.file.path, 'r') as file:
        adhics_v2 = json.load(file)

    df_v1 = preprocess_data(adhics_v1, json1_doc.version)
    df_v2 = preprocess_data(adhics_v2, json2_doc.version)
    df = pd.concat([df_v1, df_v2], ignore_index=True)

    collection = initialize_chroma_collection(df)

    final_output = generate_output(df, collection)

    return render(request, 'pdf_extractor/similarity_result.html', {'json_data': final_output})

def list_json_files(request):
    if not os.path.exists(JSON_FILES_DIR):
        os.makedirs(JSON_FILES_DIR)

    json_files = []
    for root, dirs, files in os.walk(JSON_FILES_DIR):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.relpath(os.path.join(root, file), JSON_FILES_DIR))
    
    # Debugging: Print the JSON files found
    print("JSON Files Found:", json_files)
    
    return render(request, 'pdf_extractor/list_json.html', {'json_files': json_files})


def display_json_file(request, filename):
    file_path = os.path.join(JSON_FILES_DIR, filename)
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return render(request, 'pdf_extractor/display_json.html', {'json_data': json_data})


