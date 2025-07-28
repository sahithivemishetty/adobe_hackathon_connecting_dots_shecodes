# Adobe India Hackathon 2025 - Connecting the Dots

## Team Information
- Team Name: shecodes
- **Team Members**: Sahithi Vemishetty, Sree Manaswini,Manogna Belli
- Submission Date: July 28, 2025

## Project Overview
This repository contains our solutions for the Adobe India Hackathon "Connecting the Dots" challenge. The challenge focuses on building intelligent PDF processing systems that can understand document structure and extract relevant information based on user personas.

## Challenge Description
Theme: Rethink Reading. Rediscover Knowledge


README.md – Round 1A

Adobe India Hackathon 2025
Challenge Round: 1A – Understand Your Document
Task: Structured Outline Extraction from PDFs

Problem Statement

You are given a raw PDF document. Your task is to automatically extract a structured outline, including the Title and all headings (H1, H2, H3), along with their page numbers.

Approach

PDFs do not come with semantic structure metadata, so our approach is designed to simulate how a human visually identifies section headings.

Step-by-step Workflow:

1. Text & Metadata Extraction:

We use PyMuPDF (fitz) to extract text blocks from each page, along with their bounding box positions and font size/style information.



2. Heading Identification:

Each text block is filtered by:

Font size (larger text often means headings)

Short phrase length (headings tend to be concise)

Vertical position (top-heavy blocks are likely headings)


We avoid relying only on font size, since PDFs vary — we combine heuristics.



3. Heading Classification (H1, H2, H3):

We cluster font sizes and assign heading levels (H1 > H2 > H3) based on relative font importance.

A fallback rule assigns all short top-level phrases as H1 if no differentiation is possible.



4. JSON Output Construction:

We construct a clean, hierarchical JSON with:

"title" field

"outline" list with heading level, text, and page number


Models & Libraries Used

Library	Purpose

PyMuPDF (fitz)	Fast, layout-aware PDF parsing
collections, os, json	Standard Python utilities
No ML model used	Fully heuristic and rule-based


Total dependency size is small
Offline and CPU-only compatible
Runs in <10 seconds for 50-page PDFs


 Output Format

{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}


How to Build & Run

Option 1: Using Docker (recommended for submission)

1. Build the Docker image
(from the directory containing your Dockerfile)

docker build --platform linux/amd64 -t adobe_round1a .


2. Run the container

docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe_round1a




Option 2: Run Locally without Docker

1. Install Python dependencies

pip install -r requirements.txt


2. Run the script

python main.py



Place your .pdf files in the input/ directory
The output .json will appear in the output/ directory


🧪 Constraints Met

Constraint	Status

CPU-only	yes
No internet access	yes
Runtime ≤ 10 sec	yes (tested on 50-page PDF)
Model size ≤ 200MB	yes (no model used)
JSON format compliant	yes


📁 Folder Structure

.
├── main.py                # Core script
├── requirements.txt       # Python dependencies
├── Dockerfile             # For container execution
├── input/                 # Place input PDFs here
├── output/                # JSON output will be saved here
└── README.md              # This file
