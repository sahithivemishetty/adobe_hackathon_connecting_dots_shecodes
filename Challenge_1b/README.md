

# **Adobe India Hackathon 2025 - Connecting the Dots**



### **Team Information**



Team Name: shecodes



Team Members: Sahithi Vemishetty, Sree Manaswini, Manogna Belli



Submission Date: July 28, 2025







#### **Round 1B – Persona-Driven Document Intelligence**



##### **Problem Statement**



###### Build a system that takes:



A collection of 3–10 PDFs



A defined persona (user role and background)



A job-to-be-done (task based on the persona)





###### and outputs:



The most relevant sections from the PDFs, ranked by importance



Corresponding refined sub-section content



A clean and complete JSON file with metadata





##### Approach



We simulate an intelligent assistant that filters content based on user intent. The system uses semantic embeddings and document structure to surface relevant information.

Step-by-Step Workflow:



1\. Input Handling



Reads all PDFs from input/ directory



Loads persona and job-to-be-done from persona.json







2\. Section Extraction



Uses PyMuPDF to extract text blocks



Filters short, well-positioned text blocks as heading candidates







3\. Relevance Scoring



Uses all-MiniLM-L6-v2 from sentence-transformers to embed:



Job-to-be-done description



Extracted section texts





Calculates cosine similarity and ranks sections by relevance







4\. Subsection Analysis



Extracts full page content for each top section and includes as refined\_text







5\. Output



Writes JSON with:



Metadata (persona, job, timestamp)



Extracted sections with importance ranks



Subsection analysis











##### Models \& Libraries Used



Library	Purpose



PyMuPDF	PDF parsing and section text extraction

sentence-transformers	Embedding for semantic similarity

scikit-learn	Cosine similarity computation

numpy, json, os	Utility libraries





&nbsp;CPU-only



&nbsp;Model size ≤ 1 GB



&nbsp;No internet access required



&nbsp;Runs in ≤ 60 seconds for 3–5 PDFs









&nbsp;Sample Input – persona.json

{

&nbsp; "persona": "Investment Analyst",

&nbsp; "job\_to\_be\_done": "Analyze revenue trends, R\&D investments, and market positioning strategies"

}





&nbsp;Output JSON Format



{

&nbsp; "metadata": {

&nbsp;   "input\_documents": \["report2023.pdf"],

&nbsp;   "persona": "Investment Analyst",

&nbsp;   "job\_to\_be\_done": "Analyze revenue trends...",

&nbsp;   "processing\_timestamp": "2025-07-28T17:45:00"

&nbsp; },

&nbsp; "extracted\_sections": \[

&nbsp;   {

&nbsp;     "document": "report2023.pdf",

&nbsp;     "page\_number": 4,

&nbsp;     "section\_title": "Revenue Overview",

&nbsp;     "importance\_rank": 1

&nbsp;   }

&nbsp; ],

&nbsp; "subsection\_analysis": \[

&nbsp;   {

&nbsp;     "document": "report2023.pdf",

&nbsp;     "page\_number": 4,

&nbsp;     "refined\_text": "In FY23, the company reported a 17% increase in revenue..."

&nbsp;   }

&nbsp; ]

}









##### How to Build \& Run



&nbsp;Option 1: Docker (Offline, AMD64)



docker build --platform linux/amd64 -t adobe\_round1b .

docker run --rm \\\\

&nbsp; -v $(pwd)/input:/app/input \\\\

&nbsp; -v $(pwd)/output:/app/output \\\\

&nbsp; -v $(pwd)/adobe\_solution:/app \\\\

&nbsp; --network none \\\\

&nbsp; adobe\_round1b



&nbsp;Option 2: Run Locally (Without Docker)



pip install -r requirements.txt

python main.py



> Ensure:



Your PDFs are in /input



persona.json is in the root



Output will appear in /output











##### **Constraints Met**



Constraint	            Status



CPU-only execution	    Yes

Model size ≤ 1 GB	    Yes (~90MB MiniLM)

Runtime ≤ 60s (3–5 PDFs)    Yes

No internet dependency	    Yes

Output format compliant	    Yes








