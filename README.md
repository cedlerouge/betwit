# Betwit

Sports prognosis with mean — a Django-based application for managing tournaments and user bets.

## Features
- Tournaments, teams, matches management
- User bets with rating computation and points
- Newsletter, registration
- Blog (disabled temporarily due to Django 4.2 incompatibility)

## Requirements
- Python 3.10+ recommended
- Django 4.2 LTS (pinned in requirements.txt)
- All third-party libraries are pinned to the latest stable releases compatible with Django 4.2.

## Quick start

1. Create and activate a virtualenv, then install dependencies:
   pip install -r requirements.txt

2. Set environment variables (recommended):
   - DJANGO_SECRET_KEY: a long random string
   - DJANGO_DEBUG: 1 for development, 0 for production
   - DJANGO_ALLOWED_HOSTS: comma-separated hostnames (e.g. localhost,127.0.0.1)
   - EMAIL_HOST: SMTP host (default: localhost)
   - EMAIL_PORT: SMTP port (default: 25)
   - DEFAULT_FROM_EMAIL: Default from address

   Example on Linux/macOS:
   export DJANGO_SECRET_KEY='dev-secret-please-change'
   export DJANGO_DEBUG=1
   export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

3. Initialize the database and run the server:
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver

4. Access the app at http://127.0.0.1:8000/

## API and Frontend Split

This project now exposes a REST API on /api/ for use by a separate React frontend.

- Auth: session-based via /api/auth/login/ (use Django session auth) or regular /accounts/.
- Tournaments:
  - GET /api/tournaments/
  - GET /api/tournaments/{id}/
  - GET /api/teams/
  - GET /api/matches/
- Bets (authenticated):
  - GET /api/matchbets/
  - POST /api/matchbets/ (create a bet for current user)
  - GET /api/betpoints/
  - GET /api/ratings/

CORS is enabled for http://localhost:3000 in development; configure CORS_ALLOWED_ORIGINS in settings for other hosts.

Frontend (React) recommendation:
- Create a React app in a sibling directory (e.g., frontend/) using Vite or Create React App.
- Point the React app to the API base URL (http://localhost:8000/api/).
- Implement pages that consume the API endpoints above.

## Development notes
- Settings read sensitive values from environment variables and enable basic security headers when DEBUG=0.
- Models implement __str__ and sensible default ordering for better admin usability.
- Static/media are configured for local dev; use collectstatic for production.

## Testing
Basic test scaffolding is present. Add unit tests under each app (bets/tests.py, tournaments/tests.py) and run:
python manage.py test

## Deployment
- Use gunicorn (see Procfile) and configure a proper reverse proxy (nginx).
- Set DJANGO_DEBUG=0 and configure DJANGO_ALLOWED_HOSTS.
- Run collectstatic: python manage.py collectstatic
