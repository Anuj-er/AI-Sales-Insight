# Setup & Installation

## Prerequisites
Ensure the following tools are installed on your system before proceeding:
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

You will also need:
1. A **Groq API Key** (available for free at [console.groq.com](https://console.groq.com)).
2. A **Resend API Key** (free tier at [resend.com](https://resend.com)) with a verified custom domain for email dispatch.

---

## Installation Steps

### 1. Clone the Repository
Clone the repository and navigate into the root directory:
```bash
git clone https://github.com/Anuj-er/AI-Sales-Insight.git
cd Sales-Automator
```

### 2. Configure Environment Variables
A template `.env.example` file is provided in the root directory. Copy it to initialize your local `.env` configuration.
```bash
cp .env.example .env
```
Open `.env` in a text editor and fill in your secrets:
```env
# --- LLM API Configuration ---
GROQ_API_KEY=your_groq_api_key_here

# --- Security Configuration ---
API_KEY=your_secure_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://your-vercel-app.vercel.app

# --- Email — Resend API ---
# Raw SMTP (ports 465/587) is blocked on most cloud hosts (Hugging Face, Render, etc.).
# Sign up at https://resend.com, verify a custom domain, then generate an API key.
RESEND_API_KEY=your_resend_api_key_here
SENDER_EMAIL=noreply@yourdomain.com

# --- Frontend Configuration (Vercel) ---
NEXT_PUBLIC_API_URL=https://your-hf-space.hf.space
NEXT_PUBLIC_API_KEY=your_secure_api_key_here
```

> 💡 **Why Resend instead of SMTP?** Cloud platforms such as Hugging Face Spaces block outbound SMTP ports (465/587), causing email delivery to silently fail. The backend uses the **Resend HTTP API** directly — no `smtplib` involved. Simply supply `RESEND_API_KEY` and `SENDER_EMAIL`. Sign up free at [resend.com](https://resend.com), verify your domain via DNS, and generate an API key.

### 3. Spin up the Stack
Build and launch the containerized infrastructure via Docker Compose:
```bash
docker-compose up --build -d
```
*Note: The `-d` flag runs the containers in detached mode. You can view logs using `docker-compose logs -f`.*

---

## Verifying the Deployment

### Local (Docker)
1. **Frontend UI:** Open your browser and navigate to `http://localhost:3000`. 
2. **Backend API Docs:** Navigate to `http://localhost:8000/docs`.

### Production
1. **Frontend:** Accessible at [ai-sales-in.vercel.app](https://ai-sales-in.vercel.app).
2. **Backend:** Accessible at [anuj-er-sales-insight.hf.space](https://anuj-er-sales-insight.hf.space) (append `/docs` for Swagger UI).

## Deployment Guides
For detailed steps on deploying to **Hugging Face Spaces** and **Vercel**, please refer to the main [README.md](../README.md#-production-deployment-guide).

## Shutting Down
To gracefully stop and remove the containers:
```bash
docker-compose down
```
