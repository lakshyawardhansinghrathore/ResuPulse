<div align="center">

# ResuPulse

### AI-Powered ATS Resume Analyzer & Scorer

*Know exactly why your resume gets rejected — before it does.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-Llama_3-F55036?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com)
[![Supabase](https://img.shields.io/badge/Supabase-Auth_+_DB-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Render](https://img.shields.io/badge/Render-Backend-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://resupulse-1.onrender.com/)

**🚀 [Live App](https://resupulse-g6n5fobiubjyyzridsa8pj.streamlit.app/) &nbsp;|&nbsp; 🔌 [API Docs](https://resupulse-1.onrender.com/docs) &nbsp;|&nbsp; ⭐ [GitHub](https://github.com/lakshyawardhansinghrathore/ResuPulse)**

</div>

---

## Live Deployment

| Service | URL |
|---|---|
| **Frontend (Streamlit)** | https://resupulse-g6n5fobiubjyyzridsa8pj.streamlit.app/ |
| **Backend (FastAPI on Render)** | https://resupulse-1.onrender.com/ |
| **Interactive API Docs** | https://resupulse-1.onrender.com/docs |
| **GitHub Repository** | https://github.com/lakshyawardhansinghrathore/ResuPulse |

### 🔑 Demo Account Credentials
You can test the app immediately using these demo credentials:
- **Email:** `lakshyasr7711@gmail.com`
- **Password:** `Lakshya1`

> **Note:** The backend runs on Render's free tier. The first request after inactivity may take ~30 s (cold start + lazy model loading). Subsequent requests are fast.

---

## What Makes This Different

Most ATS checkers just count keywords. **ResuPulse goes deeper.**

- **Semantic Skill Validation** — Uses sentence embeddings (`all-MiniLM-L6-v2`) to verify whether skills listed in your Skills section are actually *demonstrated* in your Projects and Experience. Just listing "Python" without evidence does not pass.
- **LLM-Powered Parsing** — Groq API (Llama 3 / GPT-OSS) extracts structured data from raw resume text — contact info, experience, education, certifications, action verbs — with an automatic 4-model fallback chain.
- **Hybrid JD Matching** — Combines fuzzy string matching (RapidFuzz, 80% threshold) with cosine similarity of dense sentence embeddings for nuanced job-description alignment.
- **Actionable Diagnostics** — Not just a score. Produces before/after rewrite examples, step-by-step action items, and severity-ranked issues tied to specific resume sections.
- **PDF Export** — Generates a multi-section executive report via Jinja2 templates and WeasyPrint.

---

## Architecture

```
User Browser
     |
     v
Streamlit Frontend (Streamlit Community Cloud)
     |  JWT Bearer Token
     v
FastAPI Backend (Render — Dockerized)
     |-- resume_parser.py      pdfplumber / python-docx  -->  raw text
     |-- groq_parser.py        Groq LLM (Llama 3)        -->  structured JSON
     |-- jd_matcher.py         SentenceTransformers + RapidFuzz  -->  JD comparison
     |-- ats_scorer.py         5-component scoring engine + penalties/bonuses
     |-- feedback_engine.py    Rule-based diagnostics     -->  IssueDetail objects
     |-- report_generator.py   Jinja2 templates           -->  PDF via WeasyPrint
     `-- supabase_db.py        httpx async client         -->  PostgreSQL (Supabase)
```

---

## Scoring System

The ATS score is a **100-point weighted composite**:

| Component | Max Score | Weight | What It Measures |
|---|---|---|---|
| **Keywords and Skills** | 25 pts | 40% | Resume keywords vs. JD, fuzzy-matched with alias normalization |
| **Content Quality** | 25 pts | 30% | Action verbs, quantifiable achievements (regex), bullet density |
| **Formatting** | 20 pts | 15% | Section detection, bullet structure, section completeness |
| **Skill Validation** | 15 pts | 40%* | Skills cross-referenced with projects/experience via embeddings |
| **ATS Compatibility** | 15 pts | 15% | Special character deductions, section brevity penalties |

*Skill Validation weight is blended into the Keywords and Skills composite.

**Penalties:** Missing JD keywords (-5 to -15 pts), address/privacy risk detected (-2 to -5 pts).
**Bonuses:** 80%+ skill validation rate (+1-2 pts), zero grammar errors (+1 pt).

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, custom CSS — hosted on Streamlit Community Cloud |
| **Backend** | FastAPI, Uvicorn, Pydantic v2 — Dockerized, hosted on Render |
| **NLP** | spaCy en_core_web_md (NER, noun chunks) |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 (CPU-only, lazy-loaded) |
| **LLM** | Groq API — Llama 3.3 70B / GPT-OSS 120B (4-model fallback chain) |
| **Fuzzy Matching** | RapidFuzz — token sort ratio with skill alias normalization |
| **PDF Export** | Jinja2 templates + WeasyPrint |
| **Auth** | Supabase — email/password + Google OAuth (JWT RS256/HS256 verified server-side) |
| **Database** | Supabase PostgreSQL via async httpx REST client |
| **File Parsing** | pdfplumber (text), PyPDF2 (hyperlink extraction), python-docx |
| **Containerization** | Docker (CPU-only PyTorch to minimize image size and RAM usage) |

---

## Project Structure

```
resupulse/
├── backend/
│   ├── api/
│   │   ├── auth.py               # JWT verification — JWKS + HS256 dual support
│   │   └── routes.py             # FastAPI router: analyze, history, PDF endpoints
│   ├── core/
│   │   └── config.py             # Env vars, model names, score weights
│   ├── database/
│   │   └── supabase_db.py        # Async save / fetch / delete via httpx
│   ├── models/
│   │   └── schemas.py            # Pydantic models: AnalysisResponse, IssueDetail, etc.
│   ├── services/
│   │   ├── ats_scorer.py         # 5-component scoring engine + skill validation
│   │   ├── feedback_engine.py    # Rule-based diagnostic system (10 issue types)
│   │   ├── groq_parser.py        # LLM resume + JD parser with retry + fallback
│   │   ├── jd_matcher.py         # Hybrid semantic + fuzzy JD comparison
│   │   ├── pdf_export.py         # WeasyPrint PDF compiler
│   │   ├── report_generator.py   # Jinja2 HTML template renderer
│   │   ├── resume_analyzer.py    # Main pipeline orchestrator
│   │   └── resume_parser.py      # File validation + text extraction
│   ├── templates/                # HTML templates for PDF report sections
│   ├── utils/
│   │   ├── file_utils.py         # Logging, error base classes, defaults
│   │   ├── matching.py           # Skill alias map + fuzzy keyword matcher
│   │   └── model_loader.py       # lru_cache lazy singletons for SpaCy + SentenceTransformer
│   ├── requirements.txt          # Backend-only dependencies
│   └── main.py                   # FastAPI app entry point
├── frontend/
│   ├── components/               # Modular Streamlit UI components
│   │   ├── dashboard.py          # Results page orchestrator
│   │   ├── detailed_feedback.py  # Collapsible diagnostic cards
│   │   ├── jd_comparison.py      # Matched / missing keyword badges
│   │   ├── score_display.py      # Score gauge + breakdown bars
│   │   └── skill_validation.py   # Validated vs. unvalidated skill tags
│   ├── services/
│   │   ├── api_client.py         # HTTP client to FastAPI (reads backend.url from st.secrets)
│   │   └── supabase_client.py    # Auth: sign-in, sign-up, Google OAuth
│   ├── views/
│   │   ├── history.py            # Past analyses view
│   │   ├── landing.py            # Home / hero page
│   │   ├── resources.py          # ATS tips and keyword guide
│   │   └── scorer.py             # Main scoring interface
│   ├── requirements.txt          # Frontend-only dependencies
│   └── streamlit_app.py          # Entry point — routing, auth state, CSS
├── jupyter notebooks/            # EDA, BERT embedding experiments, fine-tuning
├── Dockerfile                    # Backend container — CPU-only torch, WeasyPrint libs
├── .env.example
├── .gitignore
├── requirements.txt              # Combined (for local dev)
└── README.md
```

---

## Quick Start (Local)

### Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com) project
- A [Groq](https://console.groq.com) API key

### 1. Clone and set up the environment

```bash
git clone https://github.com/lakshyawardhansinghrathore/ResuPulse.git
cd ResuPulse

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

> **Linux only** — WeasyPrint requires system libraries for PDF rendering:
> ```bash
> sudo apt install -y libcairo2 libpango-1.0-0 libpangoft2-1.0-0 libffi-dev
> ```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Supabase — Project Settings -> API
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-service-role-key"
SUPABASE_ANON_KEY="your-anon-key"
SUPABASE_JWT_SECRET="your-jwt-secret"

# Groq — console.groq.com
GROQ_API_KEY="gsk_..."
```

### 4. Set up Supabase database

Run in the Supabase SQL Editor:

```sql
CREATE TABLE analyses (
  id               UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id          UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  filename         TEXT,
  ats_score        FLOAT,
  keyword_match    FLOAT,
  missing_keywords JSONB,
  analysis_result  JSONB,
  created_at       TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users manage their own analyses"
  ON analyses FOR ALL USING (auth.uid() = user_id);
```

### 5. Start the backend

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Interactive API docs at `http://localhost:8000/docs`

### 6. Start the frontend

```bash
streamlit run frontend/streamlit_app.py
```

App opens at `http://localhost:8501`

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/analyze-resume` | Required | Upload resume (PDF/DOCX) + optional JD text |
| `GET` | `/api/v1/history` | Required | Fetch all past analyses for the signed-in user |
| `DELETE` | `/api/v1/history/{id}` | Required | Delete a specific analysis entry |
| `POST` | `/api/v1/generate-pdf` | Required | Generate downloadable PDF from analysis data |
| `GET` | `/api/v1/history/{id}/pdf` | Required | Download PDF for a historical analysis |
| `GET` | `/api/v1/health` | None | Verify NLP and embedding models are loaded |

All protected endpoints require `Authorization: Bearer <supabase_access_token>`.

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_KEY` | Yes | Service role key for backend DB writes |
| `SUPABASE_ANON_KEY` | Yes | Public anon key for frontend auth |
| `SUPABASE_JWT_SECRET` | Yes | JWT secret for server-side token verification |
| `GROQ_API_KEY` | Yes | Groq Cloud API key |
| `GROQ_MODEL` | No | Override LLM model (default: openai/gpt-oss-120b) |
| `SENTENCE_TRANSFORMER_MODEL` | No | Override embedding model (default: all-MiniLM-L6-v2) |
| `FRONTEND_URL` | No | Frontend origin for CORS (default: http://localhost:8501) |

---

## Key Technical Decisions

**Why Groq over OpenAI?**
Groq LPU inference hardware delivers significantly lower latency for structured JSON extraction. The parser implements a 4-model fallback chain — if the primary model is rate-limited or unavailable, it automatically retries the next candidate without failing the request.

**Why Sentence Transformers for skill validation?**
Exact keyword matching fails for synonyms (ML vs Machine Learning, ReactJS vs React). Cosine similarity over `all-MiniLM-L6-v2` embeddings catches semantic equivalence. The 0.6 threshold is calibrated to avoid false positives while detecting genuine skill usage in freeform project descriptions.

**Why hybrid fuzzy + semantic for JD matching?**
Semantic similarity captures intent but misses exact technical terms. Fuzzy matching (token sort ratio >=80, via RapidFuzz) catches exact terms regardless of phrasing order. The final match percentage is a weighted blend: 60% keyword overlap + 40% semantic similarity.

**Why Supabase?**
Supabase provides authentication (email/password + Google OAuth), PostgreSQL with Row Level Security so users only access their own records, and a PostgREST HTTP API — without needing to build auth infrastructure from scratch.

**Why CPU-only PyTorch on Render?**
The default `sentence-transformers` install pulls in 2 GB of NVIDIA CUDA packages that are unused on a CPU-only server. Installing the `+cpu` torch wheel first tells pip that torch is already satisfied, reducing the Docker image size by ~1.8 GB and keeping runtime RAM well under Render's 512 MB free-tier limit.

---

## Sample Analysis Response

```json
{
  "ats_score": 74.5,
  "component_scores": {
    "formatting": 16.0,
    "keywords": 18.5,
    "content": 19.0,
    "skill_validation": 10.5,
    "ats_compatibility": 13.0
  },
  "issues_summary": [
    "Most Skills Lack Supporting Evidence",
    "No Quantifiable Achievements Found"
  ],
  "detailed_feedback": [
    {
      "issue_title": "Most Skills Lack Supporting Evidence",
      "severity_level": "Moderate",
      "ats_impact": "High",
      "explanation": "68% of listed skills have no mention in projects or experience.",
      "how_to_fix": "Add a project or experience bullet that uses each skill.",
      "action_items": ["Mention Redis in a project description"],
      "example_improvement": "Built a caching layer using Redis reducing API latency by 45%."
    }
  ],
  "jd_match_analysis": {
    "match_percentage": 61.3,
    "semantic_similarity": 0.743,
    "matched_keywords": ["Python", "FastAPI", "PostgreSQL"],
    "missing_keywords": ["Kubernetes", "Terraform"],
    "skills_gap": ["cloud infrastructure", "container orchestration"]
  },
  "skill_validation_details": {
    "validated": [{"skill": "Python", "projects": ["ML Sentiment Analyzer"]}],
    "unvalidated": ["Redis", "Kafka"],
    "validation_pct": 68.4
  }
}
```

---

## Roadmap

- [ ] GitHub repository URL detection — auto-validate skills from public repos
- [ ] Job board integration — auto-extract JD from LinkedIn or Naukri URL
- [ ] LLM-powered resume rewrite suggestions (not just diagnostics)
- [ ] Resume version comparison — track score improvements across iterations
- [ ] Batch analysis for multiple resumes

---

## License

MIT — free to use, fork, and build on.

---

<div align="center">

Built with **FastAPI · Streamlit · spaCy · Sentence Transformers · Groq · Supabase**

Deployed on **Render · Streamlit Community Cloud**

If this helped you, drop a star on the repo ⭐

</div>
