import fitz  # PyMuPDF
import json
import os

def extract_outline(file_path):
    doc = fitz.open(file_path)
    outline = []
    title = doc.metadata.get("title") or os.path.basename(file_path).replace(".pdf", "")

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue

                font_sizes = [span["size"] for span in spans]
                text = " ".join([span["text"] for span in spans]).strip()
                if not text:
                    continue

                max_size = max(font_sizes)

                if max_size > 20:
                    level = "H1"
                elif max_size > 16:
                    level = "H2"
                elif max_size > 13:
                    level = "H3"
                else:
                    continue

                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })

    return {
        "title": title,
        "outline": outline
    }

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            result = extract_outline(pdf_path)

            json_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(json_path, "w") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
