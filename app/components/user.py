"""
Migration of components/User.cfc → app/components/user.py

Original ColdFusion User.cfc:
  - getUsers()  access="remote" returntype="query" returnformat="json"
      SELECT id, name, email FROM users
      Returns query result as JSON.
  - addUser(name, email)  access="remote" returntype="void"
      INSERT INTO users (name, email) VALUES (?, ?)
      Uses cfqueryparam for SQL injection protection.

Python/FastAPI equivalent:
  - SQLAlchemy ORM model (User) mirrors the `users` table.
  - UserService class with get_users() and add_user() methods.
  - Pydantic schemas for request/response validation.
  - FastAPI router (app/routers/users.py) exposes the HTTP endpoints.
"""

from typing import List

from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from app.database import Base


# ---------------------------------------------------------------------------
# SQLAlchemy ORM model  (mirrors the `users` table referenced in User.cfc)
# ---------------------------------------------------------------------------

class UserModel(Base):
    """
    Mirrors the database table used in:
        SELECT id, name, email FROM users
        INSERT INTO users (name, email) VALUES (...)
    """
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name  = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)


# ---------------------------------------------------------------------------
# Pydantic schemas  (mirror cfargument / returntype)
# ---------------------------------------------------------------------------

class UserOut(BaseModel):
    """Mirrors the query columns: id, name, email (returntype="query")."""
    id:    int
    name:  str
    email: str

    class Config:
        from_attributes = True   # allows ORM → Pydantic conversion


class AddUserRequest(BaseModel):
    """
    Mirrors:
        cfargument name="name"  type="string" required="false" default=""
        cfargument name="email" type="string" required="false" default=""
    """
    name:  str = ""
    email: str = ""


# ---------------------------------------------------------------------------
# UserService  (pure business logic – no HTTP concerns)
# ---------------------------------------------------------------------------

class UserService:
    """
    Mirrors the <cfcomponent> User.cfc.

    Methods
    -------
    get_users(db) → List[UserOut]
        SELECT id, name, email FROM users
        Mirrors: cffunction name="getUsers" returntype="query"

    add_user(name, email, db) → None
        INSERT INTO users (name, email) VALUES (?, ?)
        Mirrors: cffunction name="addUser" returntype="void"
        cfqueryparam safety is handled by SQLAlchemy's parameterised queries.
    """

    @staticmethod
    def get_users(db: Session) -> List[UserOut]:
        """
        Mirrors ColdFusion:
            <cfquery name="qUsers" datasource="#application.datasource#">
                SELECT id, name, email FROM users
            </cfquery>
            <cfreturn qUsers>
        """
        rows = db.query(UserModel).all()
        return [UserOut.model_validate(row) for row in rows]

    @staticmethod
    def add_user(name: str, email: str, db: Session) -> None:
        """
        Mirrors ColdFusion:
            <cfquery datasource="#application.datasource#">
                INSERT INTO users (name, email)
                VALUES (
                    <cfqueryparam value="#arguments.name#"  cfsqltype="cf_sql_varchar">,
                    <cfqueryparam value="#arguments.email#" cfsqltype="cf_sql_varchar">
                )
            </cfquery>
        SQLAlchemy uses parameterised queries automatically (no SQL injection risk).
        """
        new_user = UserModel(name=name, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
