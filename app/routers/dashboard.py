"""
Migration of dashboard.cfm → app/routers/dashboard.py

Original ColdFusion dashboard.cfm:
  - Session guard: <cfif NOT session.isLoggedIn> <cflocation url="index.cfm">
  - Rendered a Bootstrap dashboard with a logout button and a link to users.cfm.

FastAPI equivalent:
  - GET /dashboard → enforce session guard, then render dashboard.html template.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Mirrors: dashboard.cfm

    Session guard replicates:
        <cfif NOT session.isLoggedIn>
            <cflocation url="index.cfm">
        </cfif>
    """
    if not request.session.get("isLoggedIn"):
        # Mirrors: <cflocation url="index.cfm">
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("dashboard.html", {"request": request})
