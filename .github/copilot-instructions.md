## Purpose
Short, actionable guidance for AI coding assistants working on this small Flask weather app.

## Big picture (what this repo is)
- A minimal Flask web app. The entry point is `server.py` which defines two routes (`/` and `/weather`) and renders templates.
- `weather.py` contains the integration with the OpenWeatherMap API (reads `API_KEY` from env via python-dotenv).
- UI files live under `template/` (note: singular) and static assets are in `Static/` (capitalized). These deviate from Flask defaults (`templates/` and `static/`) and are the most important gotchas.

## How to run locally
1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Create a `.env` file in the repo root with your OpenWeatherMap API key:

```text
API_KEY=your_openweathermap_key
```

3. Start the dev server (the project uses Flask debug run):

```powershell
python server.py
```

Notes: `server.py` imports `waitress.serve` but the main guard currently calls `app.run(debug=True)`. For a production-like run, start with Waitress explicitly, e.g. run a small wrapper that calls `serve(app, host='0.0.0.0', port=8080)`.

## Key integration points
- OpenWeatherMap REST API (requests) — implementation in `weather.py`.
- Environment configuration via `python-dotenv` (expects `API_KEY`).
- Templates: Jinja2 via Flask `render_template` (see `template/index.html` and `template/weather.html`).

## Project-specific conventions & quirks (explicit, do not assume defaults)
- Directory names differ from Flask defaults:
  - Templates are under `template/` (singular). If you create or modify templates, consider renaming to `templates/` or keep consistent when calling `render_template`.
  - Static files are under `Static/` (capital S). Template HTML uses `url_for('static', filename='styles.css')` which expects the `static/` folder. On Windows this may still work, but prefer renaming to `static/` for portability.
- Environment var name: `API_KEY` (see `weather.py`).
- Units: the API call in `weather.py` uses `units=imperial` — temperatures are Fahrenheit. `server.py` formats temps with one decimal place.

## Fragile spots & concrete examples to watch for
- Quoting bug in `weather.py` when building the f-string for the request URL. Example problematic line (literal from repo):

```
request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv('API_KEY')}&q={city}&units=imperial'
```

Fix approach: use double quotes for the outer f-string, or call `os.getenv('API_KEY')` into a variable first.

- Template variable mismatch: `server.py` passes `feels_like` (lowercase) but `template/weather.html` references `{{Feels_like}}` (capital F) — Jinja is case-sensitive. Keep variable names consistent.

- Template path: code calls `render_template('index.html')` but files are under `template/`. If Flask cannot find templates, either rename the directory to `templates/` or set `Flask(__name__, template_folder='template')`.

- Static asset link: templates call `url_for('static', filename='styles.css')` but static files are at `Static/styles/style.css`. Update the `url_for` path or move/rename files.

## Editing and PR guidance for AI edits
- When changing template variables, update both `server.py` and the Jinja templates to keep names identical (example: `feels_like` -> `Feels_like` or vice versa). Prefer snake_case lowercase names.
- When touching `weather.py` API call, make the API key a required env var (fail fast with clear error) and add a unit test or small script invocation to validate the JSON shape returned by OpenWeatherMap.
- Small, safe changes that improve correctness and are easy to validate:
  - Fix the f-string quoting bug in `weather.py`.
  - Rename `template/` -> `templates/` and `Static/` -> `static/` OR add `Flask(__name__, template_folder='template', static_folder='Static')` in `server.py` to preserve current layout.

## Where to look for related behavior
- `server.py` — routes, render call, debug run vs Waitress import.
- `weather.py` — API call, `load_dotenv()`, expected JSON structure (function `get_current_weather`).
- `template/index.html` and `template/weather.html` — UI, form parameters (only `city` is submitted), and static linking.

## Quick checklist for reviewers / next tasks
- Ensure `.env` contains `API_KEY`.
- Decide whether to rename directories or configure Flask to use the existing names (consistency matters).
- Standardize Jinja variable names (lowercase snake_case recommended).

---
If any section is unclear or you'd like me to (a) apply the minimal fixes (quoting bug, template/static rename vs Flask config), or (b) add a short test harness for `get_current_weather`, tell me which and I will implement it next.
