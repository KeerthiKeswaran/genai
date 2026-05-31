import os
from pypdf import PdfReader
import docx

def parse_txt_chunks(file_path, filename):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Split by double newline to get sections/paragraphs
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    chunks = []
    for b_idx, block in enumerate(blocks):
        chunks.append({
            "text": block,
            "metadata": {
                "source": filename,
                "location": f"Section {b_idx + 1}"
            }
        })
    return chunks

def parse_pdf_pages(file_path, filename):
    reader = PdfReader(file_path)
    chunks = []
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            chunks.append({
                "text": text.strip(),
                "metadata": {
                    "source": filename,
                    "location": f"Page {page_idx + 1}"
                }
            })
    return chunks

def parse_docx_paragraphs(file_path, filename):
    doc = docx.Document(file_path)
    chunks = []
    current_chunk = []
    chunk_size = 3  # Group paragraphs to avoid tiny chunks
    p_counter = 1
    
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            current_chunk.append(text)
            if len(current_chunk) >= chunk_size:
                chunks.append({
                    "text": "\n".join(current_chunk),
                    "metadata": {
                        "source": filename,
                        "location": f"Paragraphs {p_counter}-{p_counter + len(current_chunk) - 1}"
                    }
                })
                p_counter += len(current_chunk)
                current_chunk = []
                
    if current_chunk:
        chunks.append({
            "text": "\n".join(current_chunk),
            "metadata": {
                "source": filename,
                "location": f"Paragraphs {p_counter}-{p_counter + len(current_chunk) - 1}"
            }
        })
    return chunks
