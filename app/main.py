"""
Migration of Application.cfc → main.py

Original ColdFusion Application.cfc responsibilities:
  - Application name, timeout, session management, datasource config
  - onApplicationStart: initialise application-level variables
  - onSessionStart: initialise session-level variables

Python/FastAPI equivalent:
  - App configuration via environment / settings
  - Lifespan handler replaces onApplicationStart
  - Session middleware replaces ColdFusion session management
  - SQLAlchemy engine replaces <cfset this.datasource>
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.database import engine, Base
from app.routers import auth, users_router, index, dashboard

# ---------------------------------------------------------------------------
# Application settings  (mirrors <cfset this.*> block in Application.cfc)
# ---------------------------------------------------------------------------
APP_NAME = "ColdFusion AJAX DB Demo (Tag Based + Validation)"
SESSION_TIMEOUT_SECONDS = 3600          # 1 hour  (this.sessionTimeout = 0,1,0,0)
APPLICATION_TIMEOUT_SECONDS = 86400     # 1 day   (this.applicationTimeout = 1,0,0,0)
DATASOURCE = "testdemo"                 # this.datasource


# ---------------------------------------------------------------------------
# onApplicationStart equivalent – runs once at startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Replaces ColdFusion onApplicationStart."""
    # Create all DB tables if they don't exist yet
    Base.metadata.create_all(bind=engine)
    # Store app-level state (mirrors: application.appName = "...")
    app.state.app_name = APP_NAME
    yield
    # Shutdown logic would go here


# ---------------------------------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------------------------------
app = FastAPI(title=APP_NAME, lifespan=lifespan)

# Session middleware – replaces this.sessionManagement = true
# Secret key should come from an environment variable in production.
app.add_middleware(SessionMiddleware, secret_key="change-me-in-production",
                   max_age=SESSION_TIMEOUT_SECONDS,
                   https_only=False)   # mirrors this.setClientCookies = true


# ---------------------------------------------------------------------------
# onSessionStart equivalent – initialise session defaults for every new visitor
# ---------------------------------------------------------------------------
class SessionInitMiddleware(BaseHTTPMiddleware):
    """Mirrors ColdFusion onSessionStart: sets session.isLoggedIn = false."""

    async def dispatch(self, request: Request, call_next):
        if "is_logged_in" not in request.session:
            request.session["is_logged_in"] = False   # session.isLoggedIn = false
        response = await call_next(request)
        return response


app.add_middleware(SessionInitMiddleware)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(index.router)
app.include_router(dashboard.router)
app.include_router(auth.router,   prefix="/components/auth",  tags=["auth"])
app.include_router(users_router.router, prefix="/components/users", tags=["users"])
