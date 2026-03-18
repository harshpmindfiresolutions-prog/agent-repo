# ColdFusion → Python/FastAPI Migration

This repository contains the Python/FastAPI migration of a ColdFusion (CFC/CFM) web application.

## Original ColdFusion Structure

```
sample-cf/
├── Application.cfc          # App lifecycle & session config
├── index.cfm                # Login page
├── dashboard.cfm            # Dashboard page (auth-guarded)
├── users.cfm                # User management page (auth-guarded)
└── components/
    ├── Auth.cfc             # Login / logout logic
    └── User.cfc             # User CRUD (DB queries)
```

## Migrated Python/FastAPI Structure

```
agent-repo/
├── main.py                  # FastAPI app entry point (Application.cfc → main.py)
├── routers/
│   ├── auth.py              # Auth.cfc → auth router
│   └── users.py             # User.cfc → users router
├── templates/
│   ├── index.html           # index.cfm → Jinja2 login template
│   ├── dashboard.html       # dashboard.cfm → Jinja2 dashboard template
│   └── users.html           # users.cfm → Jinja2 user management template
├── database.py              # SQLAlchemy DB engine & session
├── models.py                # SQLAlchemy ORM models
└── requirements.txt         # Python dependencies
```

## Tech Stack

| Layer      | ColdFusion        | Python Equivalent         |
|------------|-------------------|---------------------------|
| Framework  | ColdFusion Server | FastAPI                   |
| Templates  | CFM pages         | Jinja2 HTML templates     |
| Database   | `<cfquery>`       | SQLAlchemy ORM            |
| Sessions   | `session` scope   | Starlette SessionMiddleware|
| JSON API   | `returnformat=json` | FastAPI JSON responses  |

## Running the App

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
