import json
import pandas as pd

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

# Display the DataFrame to ensure correctness
print(df.head())

df.to_csv('compliance_controls_data.csv', index=False)
