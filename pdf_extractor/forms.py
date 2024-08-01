from django import forms
from .models import PDFDocument, ExcelDocument

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['file']

class ExcelUploadForm(forms.ModelForm):
    sheet_name = forms.CharField(label='Sheet Name', max_length=100)
    class Meta:
        model = ExcelDocument
        fields = ['file', 'sheet_name']