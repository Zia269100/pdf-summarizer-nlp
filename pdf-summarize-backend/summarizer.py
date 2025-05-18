import fitz  # PyMuPDF
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, max_chunk=1000):
    words = text.split()
    for i in range(0, len(words), max_chunk):
        yield " ".join(words[i:i + max_chunk])

def summarize_pdf(pdf_path):
    full_text = extract_text_from_pdf(pdf_path)
    summaries = []

    for chunk in chunk_text(full_text):
        if len(chunk.strip()) > 100:  # Skip very small chunks
            summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
            summaries.append(summary[0]['summary_text'])

    return "\n\n".join(summaries)
