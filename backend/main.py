from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os

# Set up environment variables
os.environ.setdefault("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
os.environ.setdefault("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

from routers import resume, roadmap, chat

app = FastAPI(title="AI Career Compass", root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(roadmap.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "AI Career Compass Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Handler for Vercel serverless
handler = Mangum(app, lifespan="off")
