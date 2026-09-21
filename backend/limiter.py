# backend/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared Limiter instance using client IP
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])