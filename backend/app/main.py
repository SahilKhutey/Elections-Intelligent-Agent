from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routes import query, timeline, eligibility, faq, notices, announcements, stream, booths, auth, epic
from app.config import settings
from app.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject OWASP-recommended security headers into every response.
    """
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

def create_app() -> FastAPI:
    """
    Application factory to initialize the FastAPI app with middleware and routes.
    """
    app = FastAPI(
        title="Election Intelligence Assistant API",
        description="Elite, government-grade AI-powered election guidance system.",
        version="2.0.0"
    )
    
    # Rate Limiting Configuration
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "https://eia-assistant.vercel.app"],
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
        allow_credentials=True,
    )
    
    # Route Registration
    api_prefix = "/api"
    app.include_router(auth.router, prefix=api_prefix, tags=["Auth"])
    app.include_router(query.router, prefix=api_prefix, tags=["Intelligence"])
    app.include_router(timeline.router, prefix=api_prefix, tags=["Information"])
    app.include_router(eligibility.router, prefix=api_prefix, tags=["Guidance"])
    app.include_router(faq.router, prefix=api_prefix, tags=["Information"])
    app.include_router(notices.router, prefix=api_prefix, tags=["Admin"])
    app.include_router(announcements.router, prefix=api_prefix, tags=["Admin"])
    app.include_router(stream.router, prefix=api_prefix, tags=["Intelligence"])
    app.include_router(booths.router, prefix=api_prefix, tags=["Location"])
    app.include_router(epic.router, prefix=api_prefix, tags=["Guidance"])
    
    @app.get("/", tags=["Health"])
    def root():
        """Health check endpoint."""
        return {"status": "operational", "message": "EIA Intelligence Core Online"}
        
    return app

app = create_app()
