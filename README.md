# ScamSentry

Synthetic-message scam detection prototype. No real communications are ingested. See [Linear project](https://linear.app/goldiemoster/project/scamsentry-senior-scam-protection-596fe7ee3aab).

## Backend
Python 3.10+:
```
cd backend
python -m venv .venv
# Activate .venv (Windows: .venv\Scripts\activate)
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
pytest -q
```
## Frontend
Node.js 20+:
```
cd frontend
npm install
npm run dev
npm run build
```
Open http://localhost:5173. Vite proxies `/api` to http://127.0.0.1:8000.

**Safety:** heuristic risk scores are not probabilities or proof of safety. Use synthetic messages only; no authentication, production controls, Gmail or SMS access are implemented. Do not expose development servers publicly.