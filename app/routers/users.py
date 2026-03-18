"""
HTTP router for User endpoints.

Maps the ColdFusion remote-access URLs to FastAPI routes:
  GET  /components/users/getUsers  ← User.cfc?method=getUsers
  POST /components/users/addUser   ← User.cfc?method=addUser
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.components.user import AddUserRequest, UserOut, UserService
from app.database import get_db

router = APIRouter()


@router.get("/getUsers", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    """
    Mirrors: cffunction name="getUsers" access="remote" returntype="query" returnformat="json"
    Called by the front-end via: $.get("components/User.cfc?method=getUsers", ...)
    """
    return UserService.get_users(db)


@router.post("/addUser", status_code=204)
def add_user(payload: AddUserRequest, db: Session = Depends(get_db)):
    """
    Mirrors: cffunction name="addUser" access="remote" returntype="void"
    Called by the front-end via: $.post("components/User.cfc?method=addUser", ...)
    """
    UserService.add_user(name=payload.name, email=payload.email, db=db)
