"""
Migration of components/Auth.cfc → app/components/auth.py

Original ColdFusion Auth.cfc:
  - login(username, password)  access="remote" returntype="struct" returnformat="json"
      Validates hardcoded credentials (admin / 1234).
      Sets session.isLoggedIn = true on success.
      Returns {success: bool, message: str}.
  - logout()  access="remote" returntype="void"
      Clears the entire session (structClear(session)).

Python/FastAPI equivalent:
  - AuthService class with login() and logout() methods (business logic layer).
  - Pydantic schemas for request/response validation.
  - FastAPI router (app/routers/auth.py) exposes the HTTP endpoints.
"""

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Pydantic schemas  (mirror cfargument / returntype="struct")
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    """Mirrors cfargument name="username" and cfargument name="password"."""
    username: str = ""
    password: str = ""


class LoginResponse(BaseModel):
    """Mirrors the return struct {success, message}."""
    success: bool
    message: str


# ---------------------------------------------------------------------------
# AuthService  (pure business logic – no HTTP concerns)
# ---------------------------------------------------------------------------

# Hardcoded credentials matching the original ColdFusion component.
# In production these would be stored (hashed) in the database.
_VALID_USERNAME = "admin"
_VALID_PASSWORD = "1234"


class AuthService:
    """
    Mirrors the <cfcomponent> Auth.cfc.

    Methods
    -------
    login(username, password, session) → LoginResponse
        Validates credentials and sets session["is_logged_in"] = True on success.
        Mirrors: cffunction name="login" access="remote" returntype="struct"

    logout(session) → None
        Clears all session data.
        Mirrors: cffunction name="logout" access="remote" returntype="void"
    """

    @staticmethod
    def login(username: str, password: str, session: dict) -> LoginResponse:
        """
        Mirrors ColdFusion:
            <cfif arguments.username EQ "admin" AND arguments.password EQ "1234">
                <cfset session.isLoggedIn = true>
                <cfset result.success = true>
                <cfset result.message = "Login successful">
            </cfif>
            <cfreturn result>
        """
        result = LoginResponse(success=False, message="Invalid credentials")

        if username == _VALID_USERNAME and password == _VALID_PASSWORD:
            session["is_logged_in"] = True          # session.isLoggedIn = true
            result = LoginResponse(success=True, message="Login successful")

        return result

    @staticmethod
    def logout(session: dict) -> None:
        """
        Mirrors ColdFusion:
            <cfset structClear(session)>
        Clears all keys from the session dictionary.
        """
        session.clear()                             # structClear(session)
