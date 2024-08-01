import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

adhics_v1 = load_json('ADHICS_V1.json')
adhics_v2 = load_json('ADHICS_V2.json')

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

df_v1 = preprocess_data(adhics_v1, 'ADHICS_V1')
df_v2 = preprocess_data(adhics_v2, 'ADHICS_V2')
df = pd.concat([df_v1, df_v2], ignore_index=True)

df.to_csv('compliance_controls_data.csv', index=False)

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client and create a collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="controls")

# Add each row in the DataFrame to the ChromaDB collection
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

print("Data has been successfully processed and added to ChromaDB.")

# Define function to find similar controls
def find_similar_controls(query, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

# Define function to generate output
def generate_output():
    output = {}
    for index, row in df.iterrows():
        similar = find_similar_controls(row['description'])
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

# Generate the final output
final_output = generate_output()

# Write the output to a JSON file
with open('final_output.json', 'w') as f:
    json.dump(final_output, f, indent=4)

print("Final output has been written to 'final_output.json'.")
