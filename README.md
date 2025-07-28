# Adobe India Hackathon 2025 - Connecting the Dots

## Team Information
- Team Name: shecodes
- Team Members: Sahithi Vemishetty, Sree Manaswini, Manogna Belli
- Submission Date: July 28, 2025

## Overview
This repository contains solutions for the Adobe India Hackathon "Connecting the Dots" challenge, focusing on intelligent PDF processing and document analysis.

## Challenge Rounds

### Round 1A: Document Structure Extraction
- Goal: Extract structured outlines (titles, headings) from PDFs
- Location: `./round1a/`
- Key Features: Fast PDF parsing, hierarchical heading detection

### Round 1B: Persona-Driven Document Intelligence  
- Goal: Extract relevant sections based on user persona and job-to-be-done
- Location: `./round1b/`
- Key Features: Multi-document analysis, persona-based relevance ranking

## Quick Start

### Round 1A
```bash
cd round1a
docker build --platform linux/amd64 -t round1a-solution .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a-solution


# Round 1B
cd round1b
docker build --platform linux/amd64 -t round1b-solution .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b-solution