import fitz  # PyMuPDF
import json
import os

def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    title = None

    # Store average font sizes for dynamic classification
    font_sizes = []

    # Pass 1: Collect all font sizes
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        if s["size"] > 5:  # ignore very small footnotes
                            font_sizes.append(s["size"])

    # Determine thresholds for H1, H2, H3 dynamically
    unique_sizes = sorted(list(set(font_sizes)), reverse=True)
    h1_size = unique_sizes[0] if unique_sizes else 0
    h2_size = unique_sizes[1] if len(unique_sizes) > 1 else h1_size - 1
    h3_size = unique_sizes[2] if len(unique_sizes) > 2 else h2_size - 1

    # Pass 2: Extract headings
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        size = s["size"]

                        if not text or len(text.split()) > 15:
                            continue  # skip long paragraphs

                        level = None
                        if size >= h1_size:
                            level = "H1"
                            if title is None:
                                title = text  # first H1 becomes title
                        elif h2_size <= size < h1_size:
                            level = "H2"
                        elif h3_size <= size < h2_size:
                            level = "H3"

                        if level:
                            headings.append({
                                "level": level,
                                "text": text,
                                "page": page_num
                            })

    # Default title if not found
    if title is None and headings:
        title = headings[0]["text"]
    elif title is None:
        title = os.path.basename(pdf_path)

    return {"title": title, "outline": headings}


def process_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            result = extract_headings_from_pdf(pdf_path)
            json_filename = os.path.splitext(file)[0] + ".json"
            json_path = os.path.join(output_dir, json_filename)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"Processed {file} → {json_filename}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract PDF headings (H1, H2, H3) and generate JSON.")
    parser.add_argument("--input", type=str, default="input", help="Input folder containing PDFs")
    parser.add_argument("--output", type=str, default="output", help="Output folder for JSONs")
    args = parser.parse_args()

    process_pdfs(args.input, args.output)
