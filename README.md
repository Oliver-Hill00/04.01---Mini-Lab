# Canvas Dashboard (starter)

Django boilerplate for talking to the Canvas LMS REST API. The plumbing
(auth, pagination, error handling, Django wiring) is done; the actual
feature — what problem it solves and what it shows — is a TODO for you to
fill in.

## What's already wired up

- **`dashboard/canvas_api.py`** — a small Canvas client: adds the auth
  header, follows the `Link: rel="next"` header to collect every page of a
  paginated endpoint, and wraps failures (missing token, network error,
  non-2xx response) in a `CanvasAPIError` you can display to the user.
  `get_active_courses()` is a working example of the pattern.
- **`dashboard/views.py`** — a skeleton view that calls `get_active_courses()`,
  catches `CanvasAPIError`, and renders a template. Proven to work end to end.
- **`dashboard/templates/dashboard/dashboard.html`** — renders the course
  list and an error banner; has a TODO block for your actual feature.
- **`.env` / `.env.example`** — Canvas token and base URL loaded via
  `python-dotenv`, kept out of git.

## What you need to add

1. **Pick a second endpoint** (assignments, announcements, to-do list,
   upcoming events, grades — see the Canvas API docs) and write a function
   for it in `canvas_api.py`, following the `get_active_courses()` pattern
   and going through `_get_all_pages()` so pagination stays handled.
2. **Add a form field** in `dashboard/forms.py` for whatever input makes
   sense (a course picker, a date range, a keyword filter, etc.).
3. **Wire it up in `views.py`**: read the form input from `request.GET`,
   call your new endpoint function, combine/filter the data as needed.
4. **Render it in the template** as a table or list — not raw JSON.

## Setup

1. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Get a Canvas API token:** In Canvas, go to Account > Settings > scroll to
   "Approved Integrations" > "+ New Access Token". Copy it immediately —
   Canvas only shows it once.

3. **Configure `.env`:**

   ```bash
   cp .env.example .env
   ```

   Fill in `CANVAS_API_TOKEN` and `CANVAS_API_URL` (your school's Canvas
   domain, e.g. `https://yourschool.instructure.com`). `.env` is
   git-ignored — never commit it.

4. **Run it:**

   ```bash
   python manage.py runserver
   ```

   Open http://127.0.0.1:8000/ — you should see your active courses listed
   and an error banner instead of a crash if the token is wrong.
