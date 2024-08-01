from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PDFUploadForm
from .models import PDFDocument
import json
from extract_mvp import extract_text_from_pdf, process_text_to_json

def home(request):
    return render(request, 'pdf_extractor/home.html')

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = form.save()
            extracted_text = extract_text_from_pdf(pdf_document.file.path, 0, 75)
            json_output = process_text_to_json(extracted_text)
            return render(request, 'pdf_extractor/result.html', {'json_data': json.loads(json_output)})
    else:
        form = PDFUploadForm()
    return render(request, 'pdf_extractor/upload.html', {'form': form})

def query_view(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        results = process_text_to_json(query)
        return JsonResponse({'results': results})
    return render(request, 'pdf_extractor/query.html')
