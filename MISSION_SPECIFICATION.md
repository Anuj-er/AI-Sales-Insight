# 🎯 Mission Specification: Sales Insight Automator

## 📋 Context
As a newly joined **AI Cloud DevOps Engineer** at **Rabbitt AI**, you are tasked with solving a recurring bottleneck for the sales team. The team is currently overwhelmed by massive quarterly datasets (CSV/Excel) and requires a streamlined, automated solution to extract meaningful executive-level summaries.

## 🚀 Objective
Build and deploy a "Quick-Response Tool" prototype that allows team members to upload data files and instantly trigger an AI-generated brief delivered directly to their inbox.

## 🛠 Technical Requirements

### 1. Frontend: High-Fidelity User Experience
- **Single Page Application (SPA)**: Built with Next.js or React.
- **Workflow**: File upload (CSV/XLSX) + Recipient Email input.
- **Feedback**: Real-time status indicators (Loading, Success, Error).
- **Aesthetics**: Professional, minimalist corporate UI.

### 2. Backend: Secure AI Processing Layer
- **Secured API**: Protected endpoints preventing unauthorized access or resource abuse.
- **AI Integration**: Leverage LLMs (Gemini, Groq/Llama 3) to parse raw sales data into professional narratives.
- **Automated Delivery**: Integration with a mail service (SMTP/SendGrid) for report dispatch.
- **Documentation**: Live Swagger/OpenAPI endpoint for independent API validation.

### 3. Infrastructure & DevOps Excellence
- **Containerization**: Production-ready `Dockerfile` and `docker-compose.yml` for local environment parity.
- **Automation (CI/CD)**: Optimized GitHub Action for build validation and code linting.
- **Hosting**: Live deployment with separate tiers (Vercel for Frontend, Hugging Face Space for Backend).

## 📊 Evaluation Criteria
- **End-to-End Execution**: Seamless flow from upload to inbox delivery.
- **DevOps Maturity**: Image size optimization and pipeline reliability.
- **Security Posture**: Implementation of protective measures across the API boundary.
- **Architecture**: Modular codebase, clean abstractions, and robust documentation.