from fastapi import APIRouter, HTTPException, Request
from app.core.security import create_access_token
from app.limiter import limiter

router = APIRouter()

@router.post("/session")
@limiter.limit("10/minute")
async def create_session(request: Request):
    """
    Creates a stateless session token after onboarding.
    """
    try:
        data = await request.json()
        
        # In a real app, we might validate EPIC number here
        payload = {
            "user_id": "voter-" + data.get("location", "unknown"),
            "location": data.get("location"),
            "age": data.get("age"),
            "is_citizen": data.get("is_citizen", True),
            "is_resident": data.get("is_resident", True)
        }
        
        token = create_access_token(payload)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 3600
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid session request")
