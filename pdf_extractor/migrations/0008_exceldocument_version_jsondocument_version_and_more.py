# Generated by Django 5.0.7 on 2024-08-01 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_extractor', '0007_remove_jsondocument_file_path_jsondocument_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='exceldocument',
            name='version',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='jsondocument',
            name='version',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='version',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='jsondocument',
            name='file',
            field=models.FileField(default=None, upload_to='jsons/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jsondocument',
            name='original_filename',
            field=models.CharField(max_length=255),
        ),
    ]
