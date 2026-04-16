# django-auth-starter

A small Django project with user **registration**, **login**, **logout**, and optional **email notifications** on successful login and logout (via Django auth signals).

## Features

- Register, log in, log out
- Protected home page (`/`)
- Login and logout emails sent to the user’s **email address** on their account (if set)
- Environment-based configuration with `python-dotenv` (see `.env.example`)

## Requirements

- Python 3.10+ (3.12 recommended)
- Dependencies in `requirements.txt`

## Setup (local)

```bash
git clone <your-repo-url>
cd <repo-folder>
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**macOS / Linux:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Create an admin user if you need the Django admin:

```bash
python manage.py createsuperuser
```

## URLs

| URL | Description |
|-----|-------------|
| `/` | Home (requires login) |
| `/accounts/register/` | Sign up |
| `/accounts/login/` | Log in |
| `/accounts/logout/` | Log out (POST from the home page) |
| `/admin/` | Django admin |

## Email configuration

1. Copy `.env.example` to `.env` (`.env` is gitignored — **do not commit secrets**).
2. For **real SMTP** (e.g. Gmail), set `DJANGO_EMAIL_BACKEND` to Django’s SMTP backend and fill `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `DEFAULT_FROM_EMAIL`.
3. For **Gmail**, use an [App Password](https://support.google.com/accounts/answer/185833) (not your normal account password). The user record must have an **email** set, or notifications are skipped.

Using the **console** email backend prints messages in the terminal only; it does not deliver to an inbox.

## Environment variables

See `.env.example` for variables such as `SECRET_KEY`, `DEBUG`, and email-related settings. After changing `.env`, restart the development server.

## Security notes for GitHub

- Never commit `.env` or real passwords.
- Change `SECRET_KEY` and set `DEBUG=False` before any production deployment.
- Review [Django’s deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/).

## License

Add a license file if you want this repository to be clearly reusable (e.g. MIT).
