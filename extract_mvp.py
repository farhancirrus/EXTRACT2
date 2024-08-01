import PyPDF2
import re
import json

import PyPDF2
import re
import json

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
    domains = {}
    current_domain = None
    current_control = None

    for line in lines:
        domain_match = re.match(r'^(HR|AM|PE|AC|OM|CP|TP|IS|IM|CM)', line)
        control_match = re.match(r'^([A-Z]{2}\s\d+\.\d+)', line)
        label_match = re.search(r'\b(Basic|Advanced|Transitional)\b', line)

        if domain_match:
            current_domain = domain_match.group(1)
            if current_domain not in domains:
                domains[current_domain] = []
            current_control = None  # Reset current_control when a new domain is found
        if control_match:
            current_control = control_match.group(1)
            control_description = line[len(current_control):].strip()
            current_label = label_match.group(0) if label_match else "Unknown"
            domains[current_domain].append({
                "control_id": current_control,
                "control_description": control_description,
                "label": current_label
            })
        elif current_control and line.strip():
            if current_domain and domains[current_domain]:
                # Check if line contains label and split accordingly
                label_search = re.search(r'\b(Basic|Advanced|Transitional)\b', line)
                if label_search:
                    line_text = line[:label_search.start()].strip()
                    label_text = label_search.group(0)
                    domains[current_domain][-1]["control_description"] += ' ' + line_text
                    domains[current_domain][-1]["label"] = label_text
                else:
                    domains[current_domain][-1]["control_description"] += ' ' + line.strip()

    return json.dumps(domains, indent=2)

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
