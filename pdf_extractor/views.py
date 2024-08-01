from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PDFUploadForm, ExcelUploadForm
from .models import PDFDocument
import json
import logging
import pandas as pd
from extract_mvp import extract_text_from_pdf, process_text_to_json
from extract_xls import excel_to_json

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'pdf_extractor/home.html')

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = form.save()
            extracted_text = extract_text_from_pdf(pdf_document.file.path, 0, 75)
            json_output = process_text_to_json(extracted_text)
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

                # Process the Excel file to extract JSON data
                extracted_json = excel_to_json(file_path, sheet_name)

                return render(request, 'pdf_extractor/excel_result.html', {'json_data': extracted_json})
            except Exception as e:
                logger.error(f"Error processing Excel file: {e}")
                return render(request, 'pdf_extractor/upload_excel.html', {'form': form, 'error': str(e)})
        else:
            logger.error("Form is not valid")
            return render(request, 'pdf_extractor/upload_excel.html', {'form': form, 'error': 'Form is not valid'})
    else:
        form = ExcelUploadForm()
    return render(request, 'pdf_extractor/upload_excel.html', {'form': form})

def query_view(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        results = process_text_to_json(query)
        return JsonResponse({'results': results})
    return render(request, 'pdf_extractor/query.html')
