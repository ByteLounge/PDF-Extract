import os
import json
import pdfplumber
import fitz  # PyMuPDF

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_pymupdf(pdf_path):
    """Extract text using PyMuPDF"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_tables_pdfplumber(pdf_path):
    """Extract tables using pdfplumber"""
    tables_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                tables_data.append(table)
    return tables_data

def process_pdf(pdf_file):
    pdf_path = os.path.join(INPUT_DIR, pdf_file)
    extracted_text = extract_text_pymupdf(pdf_path)
    extracted_tables = extract_tables_pdfplumber(pdf_path)

    output_data = {
        "file_name": pdf_file,
        "text": extracted_text,
        "tables": extracted_tables
    }

    output_path = os.path.join(OUTPUT_DIR, f"{pdf_file.replace('.pdf', '')}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Processed: {pdf_file} → {output_path}")

def main():
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        print("❌ No PDF files found in the input folder.")
        return

    for pdf_file in pdf_files:
        process_pdf(pdf_file)

if __name__ == "__main__":
    main()
