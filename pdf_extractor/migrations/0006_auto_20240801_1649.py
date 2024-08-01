from django.db import migrations

def update_original_filenames(apps, schema_editor):
    JSONDocument = apps.get_model('pdf_extractor', 'JSONDocument')
    for doc in JSONDocument.objects.all():
        if doc.original_filename == 'unknown':
            doc.original_filename = doc.file_path.rsplit('/', 1)[-1].rsplit('.', 1)[0]
            doc.save()

class Migration(migrations.Migration):

    dependencies = [
        ('pdf_extractor', '0005_auto_20240801_1644'),
    ]

    operations = [
        migrations.RunPython(update_original_filenames),
    ]