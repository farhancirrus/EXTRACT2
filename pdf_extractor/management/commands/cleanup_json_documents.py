import os
from django.core.management.base import BaseCommand
from pdf_extractor.models import JSONDocument
from django.conf import settings

class Command(BaseCommand):
    help = 'Removes JSONDocument entries from the database if the corresponding file does not exist'

    def handle(self, *args, **options):
        for json_doc in JSONDocument.objects.all():
            file_path = json_doc.file.path
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'Deleting database entry for non-existent file: {file_path}'))
                json_doc.delete()
            else:
                self.stdout.write(self.style.SUCCESS(f'File exists: {file_path}'))

        self.stdout.write(self.style.SUCCESS('Cleanup completed successfully'))
