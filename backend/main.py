import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Import routers
from routers import resume, roadmap, chat

app = FastAPI(title="AI Career Compass")

# CORS for frontend
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

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
