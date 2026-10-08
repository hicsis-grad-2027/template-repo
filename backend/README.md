# Backend: API and database

The backend is the single source of truth. The app and the website talk only to it. It checks who the user is, stores the data, and holds the business rules.

**بالعربي:** الباك إند هو المرجع الوحيد. التطبيق والموقع بيكلّموه هو بس. هو اللي بيعرف المستخدم مين، ويخزّن الداتا، وفيه قواعد الشغل.

## Read this first

[PRINCIPLES.md](PRINCIPLES.md): five habits that make backend code safe and easy to change. Reviewers use them on every pull request.

## Start here (first time only)

Create the backend in this folder with the language your team chose (write the choice in `docs/adr/`). For example, with Python and FastAPI:

```bash
cd backend
uv init --app .
uv add fastapi uvicorn pydantic-settings
uv add --dev pytest ruff httpx
# create app/main.py with a /health route (see the layout below), then:
uv run uvicorn app.main:app --reload
```

The starter is done when it has:

- `GET /health`
- settings read from `.env` (and every setting listed in the root `.env.example`)
- `docker compose up` starting the backend and the database
- a seed script that fills the database with demo data
- at least one test, with CI green

## Every day

```bash
docker compose up        # start backend + database
uv run pytest            # run the tests
uv run ruff check .      # CI runs this
uv run ruff format .     # CI fails if code isn't formatted
```

(Use the equivalent commands for Node.js. CI detects `pyproject.toml`, `requirements.txt` or `package.json` automatically.)

## Suggested layout

```
backend/
├── app/
│   ├── main.py          # creates the app, adds the routes
│   ├── settings.py      # reads .env, fails at startup if something is missing
│   ├── routes/          # HTTP only: read the request, call a service, return a response
│   ├── services/        # the business rules
│   ├── repositories/    # the only code that talks to the database
│   └── models/          # request/response shapes and enums
├── scripts/seed.py      # demo data; running it twice gives the same result
├── tests/
└── Dockerfile
```

## Rules for this folder

- **Never trust the client.** Check the login on every request. Prices, totals and roles come from the database, never from the request.
- **Validate input at the door.** Bad input gets a clear `422`, never a `500`.
- **Assume everything runs twice.** Retries and double clicks must not create duplicates.
- **No secrets in git.** Keys go in `.env`, which is never committed.
