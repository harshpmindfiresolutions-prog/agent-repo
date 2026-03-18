"""
HTTP router for Auth endpoints.

Maps the ColdFusion remote-access URLs to FastAPI routes:
  POST /components/auth/login   ← Auth.cfc?method=login
  POST /components/auth/logout  ← Auth.cfc?method=logout
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.components.auth import AuthService, LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, request: Request):
    """
    Mirrors: cffunction name="login" access="remote" returnformat="json"
    Called by the front-end via: $.post("components/Auth.cfc?method=login", ...)
    """
    result = AuthService.login(
        username=payload.username,
        password=payload.password,
        session=request.session,
    )
    return result


@router.post("/logout")
async def logout(request: Request):
    """
    Mirrors: cffunction name="logout" access="remote" returntype="void"
    Called by the front-end via: $.post("components/Auth.cfc?method=logout", ...)
    """
    AuthService.logout(session=request.session)
    return JSONResponse(content={"success": True})
