from fastapi import Header, HTTPException, Depends
from app.core.security import verify_token
from typing import Optional

def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Dependency to extract and verify the JWT from the Authorization header.
    """
    if not authorization:
        # For a hackathon, we might allow non-auth requests but tag them as anonymous
        # For strict mode, uncomment the line below:
        # raise HTTPException(status_code=401, detail="Missing Authorization Header")
        return {"user_id": "anonymous", "location": "India"}

    try:
        # Bearer <token>
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
             raise HTTPException(status_code=401, detail="Invalid Authorization Header Format")
        
        token = parts[1]
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or Expired Token")
            
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
