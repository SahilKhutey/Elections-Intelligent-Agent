from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import query, timeline, eligibility, faq, notices, announcements
from app.config import settings

app = FastAPI(title="Election Assistant API")

# Professional CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(query.router, prefix="/api")
app.include_router(timeline.router, prefix="/api")
app.include_router(eligibility.router, prefix="/api")
app.include_router(faq.router, prefix="/api")
app.include_router(notices.router, prefix="/api")
app.include_router(announcements.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "operational", "message": "EIA Intelligence Core Online"}
