from django import forms
from .models import PDFDocument, ExcelDocument

class PDFUploadForm(forms.ModelForm):
    version = forms.CharField(max_length=50, required=True, help_text="Enter the version or tag for this document")

    class Meta:
        model = PDFDocument
        fields = ['file', 'version']

class ExcelUploadForm(forms.ModelForm):
    version = forms.CharField(max_length=50, required=True, help_text="Enter the version or tag for this document")
    sheet_name = forms.CharField(max_length=100, required=True, help_text="Enter the sheet name to process")

    class Meta:
        model = ExcelDocument
        fields = ['file', 'version', 'sheet_name']