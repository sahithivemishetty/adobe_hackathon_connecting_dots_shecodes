import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentAnalyser:
    def __init__(self, persona, job_to_be_done, model_name='all-MiniLM-L6-v2'):
        self.persona = persona
        self.job_to_be_done = job_to_be_done
        self.model = SentenceTransformer(model_name)

    def extract_sections(self, pdf_path):
        doc = fitz.open(pdf_path)
        sections = []
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("blocks")
            for block in blocks:
                text = block[4].strip()
                if text and len(text.split()) <= 12:  # Assumes short phrases are headings
                    sections.append({
                        "text": text,
                        "page": page_num,
                        "raw": page.get_text()
                    })
        return sections

    def rank_sections(self, sections):
        section_texts = [s["text"] for s in sections]
        embeddings = self.model.encode(section_texts + [self.job_to_be_done])
        section_embeddings = embeddings[:-1]
        job_embedding = embeddings[-1].reshape(1, -1)
        scores = cosine_similarity(section_embeddings, job_embedding).flatten()

        ranked = sorted(zip(sections, scores), key=lambda x: x[1], reverse=True)
        return ranked[:5]  # Return top 5 sections

    def process_document(self, pdf_path):
        sections = self.extract_sections(pdf_path)
        ranked_sections = self.rank_sections(sections)

        result = {
            "metadata": {
                "input_documents": [os.path.basename(pdf_path)],
                "persona": self.persona,
                "job_to_be_done": self.job_to_be_done,
                "processing_timestamp": str(datetime.now())
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }

        for i, (section, _) in enumerate(ranked_sections, 1):
            result["extracted_sections"].append({
                "document": os.path.basename(pdf_path),
                "page_number": section["page"],
                "section_title": section["text"],
                "importance_rank": i
            })
            result["subsection_analysis"].append({
                "document": os.path.basename(pdf_path),
                "page_number": section["page"],
                "refined_text": section["raw"]
            })

        return result


def load_persona(path="persona.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("persona", "Unknown Persona"), data.get("job_to_be_done", "Unknown Task")


def main():
    input_dir = "./input"
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    persona, job = load_persona()
    analyser = DocumentAnalyser(persona, job)

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            output = analyser.process_document(pdf_path)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(output_path, "w") as f:
                json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()