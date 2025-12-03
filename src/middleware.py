from fastapi import Request 
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from src.utils.jwt import decode_access_token

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        protected_paths = ["/me", "/protected"]

        if any(request.url.path.startswith(path) for path in protected_paths):
            token = request.cookies.get("access_token")
            if not token:
                return JSONResponse({"detail": "Missing token"}, status_code=401)

            payload = decode_access_token(token)
            if not payload or "user_id" not in payload:
                return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)

            request.state.user_id = payload["user_id"]

        response = await call_next(request)
        return response
