import pandas as pd
import json

def load_excel(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def extract_control_data(row):
    control_ref = row['Control Ref']
    if pd.notna(control_ref) and '.' in control_ref:
        control_prefix = control_ref.split(' ')[0]
        control_id = control_ref
        control_description = row['Control Requirements']
        label = row['Control Category'] if not pd.isna(row['Control Category']) else "Unknown"
        
        control_data = {
            "control_id": control_id,
            "control_description": control_description,
            "label": label
        }
        return control_prefix, control_data
    return None, None

def transform_to_json(df):
    data_json = {}
    for index, row in df.iterrows():
        control_prefix, control_data = extract_control_data(row)
        if control_prefix and control_data:
            if control_prefix not in data_json:
                data_json[control_prefix] = []
            data_json[control_prefix].append(control_data)
    return data_json

def excel_to_json(file_path, sheet_name):
    df = load_excel(file_path, sheet_name)
    data_json = transform_to_json(df)
    return json.dumps(data_json, indent=2)