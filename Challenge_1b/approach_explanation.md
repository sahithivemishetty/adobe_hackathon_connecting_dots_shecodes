### Approach Explanation

Our system is designed to extract and prioritize relevant sections from a set of PDFs based on a given persona and their specific task.

1. **Text Extraction**: We use `PyMuPDF` to extract structured text (section titles, page numbers) from PDFs.
2. **Embedding**: We use a lightweight SentenceTransformer (`all-MiniLM-L6-v2`) to embed both the persona's job-to-be-done and extracted sections.
3. **Relevance Scoring**: Cosine similarity scores are calculated between the job-to-be-done and each extracted section to rank them.
4. **Subsection Analysis**: Top-ranked sections are further analyzed and summarized into more refined, relevant content.

The model is <1GB and the solution runs under 60 seconds for 3–5 documents. It is fully CPU-compatible and does not require any internet access.
