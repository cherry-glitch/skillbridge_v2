# SkillBridge

A student skill/internship platform with a simple, feed-style UI (think Internshala's
listing feed + LinkedIn's profile/skills model), backed by PostgreSQL.

```
Register → Login → Pick branch + skills (tags, no quiz) → Feed of internships
ranked by match % → Apply → Track application status → Edit skills on Profile
```

- `backend/` — FastAPI + PostgreSQL
- `frontend/` — React + Vite + Tailwind

## Quick start

**1. PostgreSQL**: create a `skillbridge` database, then set `backend/.env` (see `backend/README.md`).

**2. Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**3. Frontend**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — register, pick a branch and some skills, and you'll land
on your feed of matched internships.

## What changed from the previous version

This replaces the earlier quiz/assessment-based design with something closer to how
Internshala and LinkedIn actually work:

- No more MCQ skill assessment — you just tag the skills you have.
- Skills are branch-aware (CSE/ECE/Mech/EEE each have their own relevant skill set, plus
  a few universal ones like Python and Git).
- The feed ranks postings by match %, and matching is branch-gated (an internship only
  open to Mechanical students won't show as eligible for a CSE student).
- A "profile strength" meter (like LinkedIn's) reflects how complete your skill tags are.
- Applying and tracking application status is now a real feature (it wasn't before).

## Fixed from your uploaded copy

- `AuthContext.jsx` was storing the auth token under a different `localStorage` key than
  `api.js` was reading from, so no authenticated request ever carried a token. Both now
  use `skillbridge_token` consistently.
- Several pages (Dashboard/Assessment/Roadmap/Matches/Applications) were calling backend
  endpoints that no longer existed after the schema was redesigned. The whole frontend has
  been rebuilt against the current backend so there's no more drift between the two.
- Added the missing "apply to internship" feature (model, endpoints, and UI) — it didn't
  exist in the backend at all before.
- Removed the unused `passlib` dependency (the code already hashes passwords with `bcrypt`
  directly) and added `pydantic[email]` since `EmailStr` needs it.
