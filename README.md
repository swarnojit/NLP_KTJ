
---

# 🧠 Enterprise Agentic Assistant (Backend)

An **intelligent, document-aware enterprise assistant** designed to understand user intent, retrieve factual answers from company documents, and trigger structured business actions like **meeting scheduling**, **ticket creation**, and **HR policy queries** — all through a simple API.

This project blends **LLMs, Retrieval-Augmented Generation (RAG), and intent detection** into a clean, production-ready backend.

---

## ✨ Why This Project Exists

In most enterprises, employees waste time:

* Searching PDFs for policies
* Asking repetitive HR questions
* Raising tickets manually
* Coordinating meetings across teams

This assistant solves that by acting as a **single conversational brain** for enterprise knowledge and workflows.

You ask questions in plain English.
The system understands **what you want**, **where to look**, and **what action to take**.

---

## 🧩 Core Capabilities

### 🔍 1. Document Intelligence (RAG)

* Reads enterprise PDFs (Annual Reports, Policies, Handbooks)
* Converts them into vector embeddings using **Sentence Transformers**
* Retrieves **only relevant sections**
* Returns **clean, factual, bullet-point answers**
* Includes **page references** for transparency

---

### 🧠 2. Intent Detection (Agentic Behavior)

The assistant **does not treat every query the same**.

It classifies user intent into:

| Intent       | Example                               |
| ------------ | ------------------------------------- |
| **MEETING**  | “Schedule a meeting with HR tomorrow” |
| **TICKET**   | “My laptop is not working”            |
| **HR**       | “How many paid leaves do I have?”     |
| **DOCUMENT** | “Explain revenue growth from page 12” |

Each intent triggers a **different execution path**.

---

### 📅 3. Smart Meeting Scheduling

* Extracts **date and time** from natural language
* Detects **department dynamically** (HR, IT, Finance, Marketing, etc.)
* Returns a structured scheduling payload

---

### 🎫 4. Ticket Creation

* Automatically creates IT support tickets
* Returns issue status and category
* Designed to plug into real ticketing systems later

---

### 👩‍💼 5. HR Policy Assistant

* Uses a **controlled LLM call**
* Returns **plain-text, factual responses**
* Prevents hallucinations and markdown noise

---

## 🏗️ System Architecture (High Level)

```
Client (UI / Frontend)
        ↓
Flask API (/chat)
        ↓
Intent Detection
        ↓
┌─────────────────────────────┐
│   MEETING / TICKET / HR     │
│        OR                   │
│   DOCUMENT (RAG Pipeline)   │
└─────────────────────────────┘
        ↓
Structured JSON Response
```

---

## 📂 Project Structure

```
.
├── app.py                 # Flask API server
├── nlp_core.py            # Core intelligence engine
├── Annual-Report-2024-25.pdf
├── .env                   # API keys
├── requirements.txt
```

---

## ⚙️ Tech Stack

* **Backend:** Flask + Flask-CORS
* **LLM Orchestration:** AutoGen
* **LLM Provider:** Google Gemini (via LiteLLM)
* **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)
* **Vector Database:** FAISS
* **PDF Parsing:** PyPDF
* **Environment Management:** python-dotenv

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/enterprise-agentic-assistant.git
cd enterprise-agentic-assistant
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### 4️⃣ Run the Server

```bash
python app.py
```

The backend will start at:

```
http://localhost:5000
```

---

## 🔌 API Usage

### **POST /chat**

**Request**

```json
{
  "message": "Schedule a meeting with finance at 3 pm"
}
```

**Response**

```json
{
  "intent": "MEETING",
  "action": "schedule_meeting",
  "department": "Finance",
  "date": "Tomorrow",
  "time": "3:00 PM",
  "priority": "High"
}
```

---

## 📖 How Document Q&A Works (RAG Flow)

1. PDF is loaded and split into meaningful text chunks
2. Text is converted into vector embeddings
3. FAISS retrieves top-K relevant chunks
4. LLM extracts **only factual points**
5. Output is cleaned, structured, and page-referenced

This ensures **accuracy over creativity** — critical for enterprise use.

---

## 🛡️ Design Principles

* ❌ No hallucinated answers
* ❌ No markdown noise
* ❌ No vague replies
* ✅ Factual, traceable, explainable responses
* ✅ Clean JSON output for frontend integration

---

## 🔮 Future Enhancements

* Calendar API integration (Google / Outlook)
* Jira / ServiceNow ticket creation
* Role-based access control
* Multi-document knowledge bases
* Streaming responses for UI
* Frontend dashboard (React / Streamlit)

---

## 👤 Author

**Swarnojit Maitra**
AI | Data Science | Generative AI
Focused on building **real-world, production-grade AI systems**

---

## 📄 Reference

* Backend server implementation: 
* Core NLP & RAG engine: 

---

If you want, I can also:

* Convert this into a **startup-style README**
* Rewrite it for **hackathon judges**
* Create a **system design diagram**
* Add **API schema documentation**
* Or tailor it for **placements / internships**

Just tell me 👍
