import PyPDF2
import re
import json
import pandas as pd

def extract_text_from_pdf(file_path, start_page, end_page):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(start_page, min(end_page + 1, len(reader.pages))):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n\n"  # Add extra newlines between pages
    return text
    
def process_text_to_json(text):
    lines = text.split('\n')
    controls = {}
    current_control = None
    
    for line in lines:
        match = re.match(r'^([A-Z]{2}\s\d+\.\d+)', line)
        if match:
            current_control = match.group(1)
            controls[current_control] = line[len(current_control):].strip()
        elif current_control and line.strip():
            controls[current_control] += ' ' + line.strip()
    
    return json.dumps(controls, indent=2)

if __name__ == "__main__":
    pdf_path = "ADHICSmvp2.pdf"
    start_page = 0  # This corresponds to page 24 in the original PDF
    end_page = 75   # This corresponds to page 100 in the original PDF
    
    extracted_text = extract_text_from_pdf(pdf_path, start_page, end_page)
    json_output = process_text_to_json(extracted_text)
    
    # Print the JSON output
    print(json_output)
    
    # Optionally, save to a file
    with open("output_multi_page.json", "w") as f:
        f.write(json_output)