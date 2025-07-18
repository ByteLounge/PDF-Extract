# Round1A - PDF Extraction

##  Approach

This module extracts **text** and **tables** from research PDFs for further processing.

- **Text extraction** → Uses **PyMuPDF (fitz)** for accurate text parsing.
- **Table extraction** → Uses **pdfplumber** to detect and structure tables.
- Output is stored as JSON files inside the `output/` folder.

---

##  **Models or Libraries Used**

- **PyMuPDF (fitz)** → High-speed text extraction.
- **pdfplumber** → Reliable table extraction.

---

##  **How to Build and Run**

### 1. Build Docker Image

```bash
docker build -t round1a:pdf_extraction .
```

### 2. Run Container
Place your PDFs in an input/ folder.


```bash
docker run --rm \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  round1a:pdf_extraction
  ```

### 3. Output
Extracted data will be saved as JSON files in the output/ folder.

Example:

```
output/
├── 2202.02958v5.json
├── 2104.11364v1.json
└── 2310.03086v1.json
```

---