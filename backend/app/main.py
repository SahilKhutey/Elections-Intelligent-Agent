from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routes import query, timeline, eligibility, faq, notices, announcements, stream, booths, auth
from app.config import settings
from app.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# OWASP Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' https://maps.googleapis.com https://maps.gstatic.com data:; "
            "script-src 'self' 'unsafe-inline' https://maps.googleapis.com; "
            "style-src 'self' 'unsafe-inline'; "
            "connect-src 'self' https://maps.googleapis.com http://localhost:8000;"
        )
        return response

app = FastAPI(title="Election Assistant API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add Security Headers
app.add_middleware(SecurityHeadersMiddleware)

# Professional CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://eia-assistant.vercel.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
)

# Route Registration
app.include_router(auth.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(timeline.router, prefix="/api")
app.include_router(eligibility.router, prefix="/api")
app.include_router(faq.router, prefix="/api")
app.include_router(notices.router, prefix="/api")
app.include_router(announcements.router, prefix="/api")
app.include_router(stream.router, prefix="/api")
app.include_router(booths.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "operational", "message": "EIA Intelligence Core Online"}
