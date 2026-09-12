# SkillBridge — Backend (FastAPI + PostgreSQL)

## Architecture (current)

- **Branches**: CSE, ECE, Mech, EEE — students belong to one.
- **Skills**: some universal (Python, Git), some branch-specific (Verilog for ECE, SolidWorks for Mech, etc.). Students pick skills as tags — no quiz.
- **Internships**: each has `eligible_branches`, required skills, and preferred skills.
- **Matching** (`app/matching.py`): branch-gated — a student outside the eligible branches scores 0 and is marked ineligible. Otherwise, score = 80% required-skill coverage + 20% preferred-skill coverage.
- **Applications**: students apply to internships and can track status (applied/shortlisted/rejected/selected).
- **Profile strength**: a simple LinkedIn-style meter (`readiness_score`), based on how many skills a student has tagged — cosmetic, separate from per-internship match score.

## Setup (PostgreSQL)

1. Make sure PostgreSQL is running locally (or use a hosted instance).
2. Create the database:
   ```sql
   CREATE DATABASE skillbridge;
   ```
3. Set `backend/.env` (already present in this project):
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/skillbridge
   SECRET_KEY=change-me-to-something-random
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ```
   Adjust the username/password/host/port to match your local Postgres setup.
4. Install and run:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate        # Windows; use source venv/bin/activate on Mac/Linux
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
   Tables and seed data (branches, skills, sample internships) are created automatically on startup.

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Key endpoints

- `POST /auth/register` `{email, password, role: "student"}`
- `POST /auth/login` `{email, password}` → `{access_token}`
- `GET /students/me` — current student profile (branch, skills, profile strength)
- `PUT /students/me/profile` `{branch_id}`
- `PUT /students/me/skills` `{skill_ids: [...]}`
- `GET /skills/branches` — list of branches
- `GET /skills?branch=cse` — universal + branch-specific skills
- `GET /internships` — all postings (public)
- `GET /internships/matches` — postings + match % for the current student (auth required)
- `POST /internships/{id}/apply` — apply
- `GET /internships/applications/me` — your application history

## Notes

- If you switch back to SQLite for quick local testing, just set `DATABASE_URL=sqlite:///./skillbridge.db` in `.env` — `database.py` detects the scheme automatically.
- `app/matching.py` is the one place to change if you want a different scoring formula later.
