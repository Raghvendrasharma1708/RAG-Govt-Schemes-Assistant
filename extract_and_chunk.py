import json
from pathlib import Path
from pypdf import PdfReader

CHUNK_SIZE = 2000      # characters (~500 tokens)
OVERLAP = 200

def extract_pages(pdf_path):
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            print(f"  Warning: could not extract page {i+1} of {pdf_path.name} ({e})")
            text = ""
        pages.append((i + 1, text))
    return pages  # it returns a pair of page_number, text_on_that_page or ''(kisi me text na ho to empty string , and also if some file is corrupted or not able to extract text then it will show the warning and return empty string for that page)

def chunk_text(text, page_num, source):   # this function will take the text and slice it into overlapping windows.
    chunks = []                           # Each slice becomes a dictionary with three fields: the actual text, which document it came from (source), and which page (page).
    start = 0                             #That metadata is the whole point — later, when our system answers a question, it can say "according to PM-KISAN, page 4" instead of just giving a vague answer.
    while start < len(text):
        piece = text[start:start + CHUNK_SIZE].strip() #start to cut out the next 2000 character
        if len(piece) > 100:   # skip tiny fragments pice under 100 characters, which are unlikely to be useful for answering questions.
            chunks.append({
                "text": piece,
                "source": source,
                "page": page_num
            })
        start += CHUNK_SIZE - OVERLAP
    return chunks

 

all_chunks = []
for pdf_file in Path("data").glob("*.pdf"):  # one by one each pdf
    source_name = pdf_file.stem            #stem grabs the file name
    print(f"Processing: {source_name}")
    for page_num, text in extract_pages(pdf_file): # on each page of the pdf, extract the text and chunk it
        all_chunks.extend(chunk_text(text, page_num, source_name))

print(f"\nTotal chunks: {len(all_chunks)}")

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)