from django.db import models

class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs/')
    version = models.CharField(max_length=50, default='unknown')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExcelDocument(models.Model):
    file = models.FileField(upload_to='excels/')
    version = models.CharField(max_length=50, default='unknown')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class JSONDocument(models.Model):
    file = models.FileField(upload_to='jsons/')
    original_filename = models.CharField(max_length=255)
    version = models.CharField(max_length=50, default='unknown')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_filename} - {self.version}"
