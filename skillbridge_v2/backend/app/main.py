from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .seed_data import seed
from .routers import auth, students, skills, internships

# Ensure tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillBridge API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Run seeder on startup
    seed()

# Include Routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(skills.router)
app.include_router(internships.router)

@app.get("/")
def root():
    return {"message": "SkillBridge API is online"}