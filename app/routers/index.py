"""
Migration of index.cfm → app/routers/index.py

Original ColdFusion index.cfm:
  - Rendered a login page (HTML + jQuery AJAX).
  - No server-side session guard (it IS the login page).

FastAPI equivalent:
  - GET  /        → render login template (index.html).
  - If the user is already logged in, redirect to /dashboard.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Mirrors: index.cfm (the login page).

    If the session already has isLoggedIn=True we redirect to /dashboard,
    mirroring the implicit ColdFusion behaviour where a logged-in user
    visiting index.cfm would be bounced by dashboard.cfm's guard.
    """
    if request.session.get("isLoggedIn"):
        return RedirectResponse(url="/dashboard", status_code=302)

    # Pass any flash message set by a failed login attempt
    flash_message = request.session.pop("flash_message", None)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "flash_message": flash_message},
    )
