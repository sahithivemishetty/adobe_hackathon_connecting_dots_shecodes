import re
from typing import List, Dict, Any
import fitz  # PyMuPDF


class OutlineExtractor:
    def __init__(self):
        self.heading_patterns = [
            r'^\d+\.\s+.+$',              # 1. Introduction
            r'^\d+\.\d+\s+.+$',           # 1.1 Overview
            r'^\d+\.\d+\.\d+\s+.+$',      # 1.1.1 Subsection
            r'^[A-Z][A-Z\s]+$',           # ALL CAPS
            r'^[IVX]+\.\s+.+$',           # Roman numerals
            r'^[A-Z]\.\s+.+$',            # A. Heading
            r'^\([a-z]\)\s+.+$',          # (a) point
        ]

    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        doc = fitz.open(pdf_path)
        title = self.extract_title(doc)
        headings = self.extract_headings(doc)
        return {
            "title": title,
            "headings": headings
        }

    def extract_title(self, doc) -> str:
        """Extract title from the first page based on largest font size."""
        first_page = doc[0]
        blocks = first_page.get_text("dict")["blocks"]
        candidates = []

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if len(text.split()) < 3:
                        continue
                    if any(word in text.lower() for word in ["page", "contents", "abstract"]):
                        continue
                    candidates.append((text, span["size"]))

        if not candidates:
            return "Document Title"

        # Return the text with the largest font size
        return sorted(candidates, key=lambda x: x[1], reverse=True)[0][0]

    def extract_headings(self, doc) -> List[Dict[str, Any]]:
        """Extract headings from all pages using font size and regex patterns."""
        headings = []

        for i, page in enumerate(doc):
            text = page.get_text("dict")
            plain_text = page.get_text("text")

            # Pattern-based headings from plain text
            for line in plain_text.splitlines():
                for pattern in self.heading_patterns:
                    if re.match(pattern, line.strip()):
                        headings.append({
                            "text": line.strip(),
                            "page": i + 1,
                            "method": "pattern"
                        })
                        break

            # Font-based large text detection
            for block in text["blocks"]:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] >= 13 and len(span["text"].split()) <= 10:
                            headings.append({
                                "text": span["text"].strip(),
                                "page": i + 1,
                                "method": "font"
                            })

        # Remove duplicates
        seen = set()
        final_headings = []
        for h in headings:
            key = (h["text"].lower(), h["page"])
            if key not in seen:
                final_headings.append(h)
                seen.add(key)

        return final_headings