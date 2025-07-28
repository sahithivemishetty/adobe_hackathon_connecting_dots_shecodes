import os
import json
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if text and len(text.split()) <= 12:  # basic heading filter
                sections.append({
                    "text": text,
                    "page": page_num,
                    "raw": page.get_text()
                })
    return sections

def rank_sections(sections, persona_job, model):
    section_texts = [s["text"] for s in sections]
    embeddings = model.encode(section_texts + [persona_job])
    section_embeddings = embeddings[:-1]
    job_embedding = embeddings[-1].reshape(1, -1)

    scores = cosine_similarity(section_embeddings, job_embedding).flatten()
    ranked = sorted(zip(sections, scores), key=lambda x: x[1], reverse=True)
    return ranked[:5]  # Top 5 sections

def process_document(pdf_file, persona, job, model):
    sections = extract_sections(pdf_file)
    ranked_sections = rank_sections(sections, job, model)

    output = {
        "metadata": {
            "input_documents": [os.path.basename(pdf_file)],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": str(datetime.now())
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for i, (section, score) in enumerate(ranked_sections, 1):
        output["extracted_sections"].append({
            "document": os.path.basename(pdf_file),
            "page_number": section["page"],
            "section_title": section["text"],
            "importance_rank": i
        })
        output["subsection_analysis"].append({
            "document": os.path.basename(pdf_file),
            "page_number": section["page"],
            "refined_text": section["raw"]
        })

    return output

def main():
    input_dir = "./input"
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    # Load persona/job-to-be-done
    with open("persona.json", "r") as f:
        persona_data = json.load(f)

    persona = persona_data.get("persona", "Unknown Persona")
    job = persona_data.get("job_to_be_done", "Unknown Task")

    model = SentenceTransformer('all-MiniLM-L6-v2')

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            output_data = process_document(pdf_path, persona, job, model)
            out_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(out_path, "w") as f:
                json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    main()
