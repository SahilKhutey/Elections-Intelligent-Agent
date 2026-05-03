import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Disable rate limiting if TESTING is true in environment
is_testing = os.getenv("TESTING", "false").lower() == "true"

limiter = Limiter(
    key_func=get_remote_address,
    enabled=not is_testing
)
