"""
Migration of users.cfm → app/routers/users_page.py

Original ColdFusion users.cfm:
  - Session guard: <cfif NOT session.isLoggedIn> <cflocation url="index.cfm">
  - Rendered a Bootstrap page with an Add-User form and a user list table.
  - AJAX called User.cfc?method=getUsers and User.cfc?method=addUser.

FastAPI equivalent:
  - GET /users → enforce session guard, then render users.html template.
  - The AJAX endpoints themselves live in app/routers/users.py
    (migrated from components/User.cfc).
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """
    Mirrors: users.cfm

    Session guard replicates:
        <cfif NOT session.isLoggedIn>
            <cflocation url="index.cfm">
        </cfif>
    """
    if not request.session.get("isLoggedIn"):
        # Mirrors: <cflocation url="index.cfm">
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("users.html", {"request": request})
