# Adobe India Hackathon 2025 - Connecting the Dots

## 🧠 Team Information
- **Team Name:** shecodes
- **Team Members:** Sahithi Vemishetty, Sree Manaswini, Manogna Belli
- **Submission Date:** July 28, 2025

---

## 🔍 Overview
This repository contains our solutions for the **Adobe India Hackathon 2025** under the theme *"Connecting the Dots"*. The project focuses on intelligent PDF processing and persona-driven document analysis.

---

## 🧩 Challenge Rounds

### 📄 Round 1A: Document Structure Extraction
- **Objective:** Extract structured outlines (titles, headings, subheadings) from PDF documents.
- **Folder:** [`round1a/`](./round1a/)
- **Key Features:**
  - Fast and lightweight PDF parsing
  - Hierarchical heading detection
  - Structured JSON output

---

### 👤 Round 1B: Persona-Driven Document Intelligence
- **Objective:** Extract and rank relevant sections from multiple PDFs based on user persona and job-to-be-done.
- **Folder:** [`round1b/`](./round1b/)
- **Key Features:**
  - Multi-document ingestion and processing
  - Persona-based section filtering
  - Relevance-based ranking of extracted content

---

## 🚀 Quick Start

> Ensure Docker is installed on your system.

### ▶️ Round 1A
```bash
cd round1a
docker build --platform linux/amd64 -t round1a-solution .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a-solution
