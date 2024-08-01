import json
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from django.conf import settings
from pdf_extractor.models import JSONDocument
from django.core.files import File

def save_json(data, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'jsons', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    return file_path

def save_json_document(json_data, original_filename, version):
    filename = f'{original_filename}_{version}.json'
    file_path = os.path.join(settings.MEDIA_ROOT, 'jsons', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)
    
    with open(file_path, 'rb') as f:
        django_file = File(f)
        json_document = JSONDocument(original_filename=original_filename, version=version)
        json_document.file.save(filename, django_file, save=True)
    
    return json_document

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def preprocess_data(data, version):
    rows = []
    for domain, controls in data.items():
        for control in controls:
            rows.append({
                'domain': domain,
                'control_id': control['control_id'],
                'description': control['control_description'],
                'label': control['label'],
                'version': version
            })
    return pd.DataFrame(rows)


def initialize_chroma_collection(df):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="controls")

    for index, row in df.iterrows():
        embedding = model.encode(row['description']).tolist()
        collection.add(
            documents=[row['description']],
            metadatas=[{
                'domain': row['domain'],
                'control_id': row['control_id'],
                'version': row['version']
            }],
            ids=[str(index)]
        )
    return collection

def find_similar_controls(query, collection, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def generate_output(df, collection):
    output = {}
    for index, row in df.iterrows():
        similar = find_similar_controls(row['description'], collection)
        tags = set([row['version']] + [m['version'] for m in similar['metadatas'][0]])
        control_data = {
            'control_id': row['control_id'],
            'description': row['description'],
            'tags': list(tags)
        }
        if row['domain'] not in output:
            output[row['domain']] = []
        output[row['domain']].append(control_data)
    return output
