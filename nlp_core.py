# import os
# import re
# import sys
# from datetime import datetime
# from dotenv import load_dotenv

# # --------- AutoGen + LiteLLM ----------
# import autogen
# import litellm

# # --------- RAG ----------
# from pypdf import PdfReader
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np

# # ================= CONFIG =================
# load_dotenv()
# litellm.suppress_debug_info = True

# PDF_PATH = "Annual-Report-2024-25.pdf"
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_KEY:
#     print("❌ Error: GEMINI_API_KEY not found in environment.")
#     sys.exit(1)

# # ================= PDF LOAD =================
# print(f"📄 Loading Knowledge Base ({PDF_PATH})...")
# try:
#     if not os.path.exists(PDF_PATH):
#         print("⚠️ PDF not found. Using Mock Data.")
#         texts = ["Company policy allows 20 days paid leave."]
#         meta = [{"page": 1}]
#         TOTAL_PAGES = 1
#     else:
#         reader = PdfReader(PDF_PATH)
#         TOTAL_PAGES = len(reader.pages)
#         texts, meta = [], []
#         for i, page in enumerate(reader.pages):
#             text = page.extract_text()
#             if text and len(text.strip()) > 50:
#                 texts.append(text)
#                 meta.append({"page": i + 1})
# except Exception as e:
#     print(f"❌ Error reading PDF: {e}")
#     sys.exit(1)

# # ================= VECTOR DB =================
# print("🧠 Building Vector Index...")
# embedder = SentenceTransformer("all-MiniLM-L6-v2")
# embeddings = embedder.encode(texts, convert_to_numpy=True)
# index = faiss.IndexFlatL2(embeddings.shape[1])
# index.add(embeddings)
# print("✅ System Ready!\n")

# def vector_search(query, k=4):
#     q_emb = embedder.encode([query], convert_to_numpy=True)
#     _, idxs = index.search(q_emb, k)
#     results = []
#     for i in idxs[0]:
#         if i < len(texts):
#             results.append({"page": meta[i]["page"], "text": texts[i]})
#     return results

# # ================= AUTOGEN CONFIG =================
# llm_config = {
#     "config_list": [{
#         "model": "gemini-2.5-flash", # Stable model
#         "api_key": GEMINI_KEY,
#         "api_type": "google"
#     }],
#     "temperature": 0,
#     "cache_seed": None
# }

# assistant = autogen.AssistantAgent(
#     name="enterprise_agent",
#     system_message="You are a helpful corporate assistant. Extract facts accurately.",
#     llm_config=llm_config,
#     human_input_mode="NEVER"
# )

# def autogen_call(prompt):
#     """Safely calls AutoGen and returns a String."""
#     try:
#         reply = assistant.generate_reply(
#             messages=[{"role": "user", "content": prompt}]
#         )
#         if isinstance(reply, dict):
#             return str(reply.get("content", ""))
#         return str(reply)
#     except Exception as e:
#         return f"Error: {str(e)}"

# # ================= HELPERS =================
# def extract_page_number(text):
#     m = re.search(r'page\s*(\d+)', text.lower())
#     return int(m.group(1)) if m else None

# def get_page_text(page_no):
#     if 1 <= page_no <= TOTAL_PAGES:
#         if not texts and TOTAL_PAGES == 1: return texts[0]
#         try:
#             return reader.pages[page_no - 1].extract_text()
#         except: return None
#     return None

# def format_as_points(text, page_no, max_points=8):
#     # Split text into sentences
#     sentences = re.split(r'(?<=[.!?])\s+', text)
#     points = []
#     for s in sentences:
#         s = s.strip()
#         if len(s) < 15: continue
        
#         # REMOVE ALL STARS (*) AND HASHES (#) to clean output
#         clean_s = s.replace("*", "").replace("#", "").strip()
        
#         points.append({
#             "point": clean_s,
#             "page": page_no
#         })
#         if len(points) >= max_points: break
#     return points

# def extract_date_time(text):
#     text = text.lower()
#     date, time = None, None
#     tm = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', text)
#     if tm:
#         h, m, p = int(tm.group(1)), tm.group(2) or "00", tm.group(3)
#         time = f"{h}:{m} {p.upper()}"
    
#     dm = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', text)
#     if dm:
#         day = int(dm.group(1))
#         month = dm.group(2).capitalize()
#         year = datetime.now().year
#         date = f"{day}-{month}-{year}"
        
#     return date, time

# def detect_intent(q):
#     q = q.lower()
#     if any(k in q for k in ["meeting", "schedule", "call", "book"]): return "MEETING"
#     if any(k in q for k in ["ticket", "issue", "problem", "broken"]): return "TICKET"
#     if any(k in q for k in ["leave", "policy", "salary", "promotion"]): return "HR"
#     return "DOC"

# # ================= MAIN LOGIC =================
# # ================= MAIN LOGIC =================
# def process_query(query: str) -> dict:
#     intent = detect_intent(query)
#     query_lower = query.lower()

#     # -------- MEETING --------
#     if intent == "MEETING":
#         date, time = extract_date_time(query)
        
#         # 1. Detect Department Dynamically
#         department = "General" # Default if nothing specified
#         if "finance" in query_lower:
#             department = "Finance"
#         elif "hr" in query_lower:
#             department = "HR"
#         elif "it" in query_lower or "tech" in query_lower:
#             department = "IT"
#         elif "boss" in query_lower or "manager" in query_lower:
#             department = "Management"
#         elif "sales" in query_lower:
#             department = "Sales"
#         elif "marketing" in query_lower:
#             department = "Marketing"

#         msg = f"Meeting scheduled with {department} for {time or '10:00 AM'} on {date or 'Tomorrow'}."
        
#         return {
#             "intent": "MEETING",
#             "action": "schedule_meeting",
#             "department": department,  # <--- Now Dynamic
#             "date": date if date else "Tomorrow",
#             "time": time if time else "10:00 AM",
#             "priority": "High",
#             "answer": msg 
#         }

#     # -------- TICKET --------
#     if intent == "TICKET":
#         msg = f"Ticket raised for: '{query}'. Status: Open."
#         return {
#             "intent": "TICKET",
#             "action": "create_ticket",
#             "category": "IT Support",
#             "issue": query,
#             "status": "Open",
#             "answer": msg 
#         }

#     # -------- HR --------
#     if intent == "HR":
#         reply = autogen_call(f"You are an HR assistant. Answer strictly in plain text without using stars or markdown.\n\n{query}")
#         clean_reply = str(reply).replace("*", "").strip()
#         return {
#             "intent": "HR",
#             "answer": clean_reply
#         }

#     # -------- PAGE LOCK --------
#     page_no = extract_page_number(query)
#     if page_no:
#         page_text = get_page_text(page_no)
#         if not page_text:
#             return {"intent": "DOCUMENT", "answer": f"Page {page_no} not found."}

#         raw = autogen_call(f"Extract ONLY factual points. Do not use markdown.\n\n{page_text}\n\nQuestion:{query}")
#         points = format_as_points(raw, page_no)
        
#         formatted_text = "\n".join([f"- {p['point']}" for p in points])
        
#         return {
#             "intent": "DOCUMENT",
#             "answer": formatted_text,
#             "sources": [page_no]
#         }

#     # -------- NORMAL RAG --------
#     docs = vector_search(query)
#     all_points = []
#     pages = []

#     for d in docs:
#         raw = autogen_call(f"Extract ONLY relevant facts. Do not use markdown.\n\n{d['text']}\n\nQuestion:{query}")
#         pts = format_as_points(raw, d["page"])
#         if pts:
#             all_points.extend(pts)
#             pages.append(d["page"])

#     if all_points:
#         formatted_text = "\n".join([f"- {p['point']} (Pg {p['page']})" for p in all_points])
#     else:
#         formatted_text = "No relevant facts found in the document."

#     return {
#         "intent": "DOCUMENT",
#         "answer": formatted_text,
#         "sources": sorted(set(pages))
#     }

import os
import re
import sys
from datetime import datetime
from dotenv import load_dotenv

# --------- AutoGen + LiteLLM ----------
import autogen
import litellm

# --------- RAG ----------
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ================= CONFIG =================
load_dotenv()
litellm.suppress_debug_info = True

PDF_PATH = "Annual-Report-2024-25.pdf"
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("❌ Error: GEMINI_API_KEY not found in environment.")
    sys.exit(1)

# ================= PDF LOAD =================
print(f"📄 Loading Knowledge Base ({PDF_PATH})...")
try:
    if not os.path.exists(PDF_PATH):
        print("⚠️ PDF not found. Using Mock Data.")
        texts = ["Company policy allows 20 days paid leave."]
        meta = [{"page": 1}]
        TOTAL_PAGES = 1
    else:
        reader = PdfReader(PDF_PATH)
        TOTAL_PAGES = len(reader.pages)
        texts, meta = [], []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and len(text.strip()) > 50:
                texts.append(text)
                meta.append({"page": i + 1})
except Exception as e:
    print(f"❌ Error reading PDF: {e}")
    sys.exit(1)

# ================= VECTOR DB =================
print("🧠 Building Vector Index...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedder.encode(texts, convert_to_numpy=True)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
print("✅ System Ready!\n")

def vector_search(query, k=4):
    q_emb = embedder.encode([query], convert_to_numpy=True)
    _, idxs = index.search(q_emb, k)
    results = []
    for i in idxs[0]:
        if i < len(texts):
            results.append({"page": meta[i]["page"], "text": texts[i]})
    return results

# ================= AUTOGEN CONFIG =================
llm_config = {
    "config_list": [{
        "model": "gemini-2.5-flash", # Stable model
        "api_key": GEMINI_KEY,
        "api_type": "google"
    }],
    "temperature": 0,
    "cache_seed": None
}

assistant = autogen.AssistantAgent(
    name="enterprise_agent",
    system_message="You are a helpful corporate assistant. Extract facts accurately.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

def autogen_call(prompt):
    """Safely calls AutoGen and returns a String."""
    try:
        reply = assistant.generate_reply(
            messages=[{"role": "user", "content": prompt}]
        )
        if isinstance(reply, dict):
            return str(reply.get("content", ""))
        return str(reply)
    except Exception as e:
        return f"Error: {str(e)}"

# ================= HELPERS =================
def extract_page_number(text):
    m = re.search(r'page\s*(\d+)', text.lower())
    return int(m.group(1)) if m else None

def get_page_text(page_no):
    if 1 <= page_no <= TOTAL_PAGES:
        if not texts and TOTAL_PAGES == 1: return texts[0]
        try:
            return reader.pages[page_no - 1].extract_text()
        except: return None
    return None

def format_as_points(text, page_no, max_points=8):
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    points = []
    for s in sentences:
        s = s.strip()
        if len(s) < 15: continue
        
        # REMOVE ALL STARS (*) AND HASHES (#) to clean output
        clean_s = s.replace("*", "").replace("#", "").strip()
        
        points.append({
            "point": clean_s,
            "page": page_no
        })
        if len(points) >= max_points: break
    return points

def extract_date_time(text):
    text = text.lower()
    date, time = None, None
    tm = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', text)
    if tm:
        h, m, p = int(tm.group(1)), tm.group(2) or "00", tm.group(3)
        time = f"{h}:{m} {p.upper()}"
    
    dm = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', text)
    if dm:
        day = int(dm.group(1))
        month = dm.group(2).capitalize()
        year = datetime.now().year
        date = f"{day}-{month}-{year}"
        
    return date, time

def detect_intent(q):
    q = q.lower()
    if any(k in q for k in ["meeting", "schedule", "call", "book"]): return "MEETING"
    if any(k in q for k in ["ticket", "issue", "problem", "broken"]): return "TICKET"
    if any(k in q for k in ["leave", "policy", "salary", "promotion"]): return "HR"
    return "DOC"

# ================= MAIN LOGIC =================
def process_query(query: str) -> dict:
    intent = detect_intent(query)
    query_lower = query.lower()

    # -------- MEETING --------
    if intent == "MEETING":
        date, time = extract_date_time(query)
        
        # Detect Department Dynamically
        department = "General"
        if "finance" in query_lower:
            department = "Finance"
        elif "hr" in query_lower:
            department = "HR"
        elif "it" in query_lower or "tech" in query_lower:
            department = "IT"
        elif "boss" in query_lower or "manager" in query_lower:
            department = "Management"
        elif "sales" in query_lower:
            department = "Sales"
        elif "marketing" in query_lower:
            department = "Marketing"
        
        return {
            "intent": "MEETING",
            "action": "schedule_meeting",
            "department": department,
            "date": date if date else "Tomorrow",
            "time": time if time else "10:00 AM",
            "priority": "High"
        }

    # -------- TICKET --------
    if intent == "TICKET":
        return {
            "intent": "TICKET",
            "action": "create_ticket",
            "category": "IT Support",
            "issue": query,
            "status": "Open"
        }

    # -------- HR --------
    if intent == "HR":
        reply = autogen_call(f"You are an HR assistant. Answer strictly in plain text without using stars or markdown.\n\n{query}")
        clean_reply = str(reply).replace("*", "").strip()
        return {
            "intent": "HR",
            "answer": clean_reply
        }

    # -------- PAGE LOCK --------
    page_no = extract_page_number(query)
    if page_no:
        page_text = get_page_text(page_no)
        if not page_text:
            return {
                "intent": "DOCUMENT", 
                "answer": f"Page {page_no} not found.",
                "sources": []
            }

        raw = autogen_call(f"Extract ONLY factual points. Do not use markdown.\n\n{page_text}\n\nQuestion:{query}")
        points = format_as_points(raw, page_no)
        
        formatted_text = "\n".join([f"- {p['point']}" for p in points])
        
        return {
            "intent": "DOCUMENT",
            "answer": formatted_text if formatted_text else "No relevant information found on this page.",
            "sources": [page_no]
        }

    # -------- NORMAL RAG --------
    docs = vector_search(query)
    all_points = []
    pages = []

    for d in docs:
        raw = autogen_call(f"Extract ONLY relevant facts. Do not use markdown.\n\n{d['text']}\n\nQuestion:{query}")
        pts = format_as_points(raw, d["page"])
        if pts:
            all_points.extend(pts)
            if d["page"] not in pages:
                pages.append(d["page"])

    if all_points:
        formatted_text = "\n".join([f"- {p['point']}" for p in all_points])
    else:
        formatted_text = "No relevant facts found in the document."

    return {
        "intent": "DOCUMENT",
        "answer": formatted_text,
        "sources": sorted(set(pages))
    }