# Setup & Installation

## Prerequisites
Ensure the following tools are installed on your system before proceeding:
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

You will also need:
1. A **Groq API Key** (available for free at [console.groq.com](https://console.groq.com)).
2. An **App Password** for an SMTP provider (e.g., Gmail App Passwords, SendGrid, Mailgun) to dispatch emails.

---

## Installation Steps

### 1. Clone the Repository
Clone the repository and navigate into the root directory:
```bash
git clone <repository_url>
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

# --- Email (SMTP) Configuration ---
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# --- Security Configuration ---
# Generate a secure 64-character hex string or use any secure secret.
API_KEY=your_secure_api_key
```

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
