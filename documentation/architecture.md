# System Architecture

## Overview
The Sales Insight Automator is designed using a decoupled, containerized architecture separating the client-side single-page application from the heavy computational and API orchestration backend.

## Components

### 1. Frontend (Next.js 14)
- **Framework:** Next.js (App Router)
- **Role:** Single Page Application (SPA) providing the user interface.
- **Styling:** TailwindCSS for minimal, professional corporate styling.
- **Containerization:** Built into a highly optimized, static asset Docker image served via Node.js alpine.

### 2. Backend (FastAPI)
- **Framework:** FastAPI (Python 3.11)
- **Role:** REST API server handling file ingestion, data processing, external API calls, and email dispatch.
- **Data Parsing:** `pandas` and `openpyxl` are utilized to extract and synthesize raw CSV/XLSX structures into summarized prompt contexts.
- **Security:** Custom middleware intercepts requests to validate the `X-API-Key` header against the system's environment variables.

### 3. AI Middleware (Groq)
- **Provider:** Groq Cloud
- **Model:** `llama-3.1-8b-instant`
- **Role:** Ingests serialized data summaries and prompts to formulate human-readable, executive-level narratives. Selected for its exceptionally low latency (blazing fast inference speeds).

### 4. Email Dispatch Service
- **Provider:** [Resend](https://resend.com) HTTP API.
- **Role:** Takes the Markdown payload from Groq, converts it into a styled HTML email, and dispatches it to the recipient's inbox via a single authenticated `POST https://api.resend.com/emails` call.
- **Why not SMTP?** Cloud hosts (Hugging Face Spaces, Render, etc.) block outbound SMTP ports (465/587). The Resend HTTP API bypasses this entirely and works reliably from any hosting environment.

## Data Flow Diagram
*(Refer to the main `README.md` for visual system architecture flows).*
