from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload
import os

app = FastAPI(
    title="Sales Insight Automator API",
    description="API for parsing sales data and generating AI summaries.",
    version="1.0.0"
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Sales Insight Automator API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
