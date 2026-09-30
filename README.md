# DK Fashions

A full-stack Django fashion boutique — browse 8 clothing categories, search,
add to cart, apply the promo code, and check out. Accounts are confirmed with
a 6-digit email code, and the dashboard shows your recent searches, the store's
most-searched terms, and best-selling products. Admins can grant other users
admin privileges.

Built with Django 6.1, a bright editorial theme (Fraunces + Inter), and
WhiteNoise for static files.

## Features
- **Storefront:** home, category grid (8 categories), product catalogue with
  search + filter + sort, product detail pages.
- **Cart & checkout:** session cart, quantity controls, promo code
  **`NUST000`** for 20% off, order confirmation.
- **Accounts:** email-based sign up / log in, **email verification code**,
  member dashboard.
- **Dashboard analytics:** your recent searches, most-searched terms, and
  most-bought products.
- **Admin:** Django admin at `/admin/`, plus an in-app **Manage users** page
  where a superuser can grant/revoke admin rights.

## Run it (Windows)
From this folder (`Desktop\dk_fashions`):

    "C:\Users\redee\anaconda3\python.exe" manage.py migrate
    "C:\Users\redee\anaconda3\python.exe" manage.py seed
    "C:\Users\redee\anaconda3\python.exe" manage.py runserver

Then open http://127.0.0.1:8000/ — or just double-click **Start-App.bat**.

### Admin / owner account
Already created:

- Email: `redeemertafadzwa@gmail.com`
- Password: `DkAdmin2026!`  *(change this — see below)*

Log in, open **Dashboard → Manage users** to grant admin to others, or use the
Django admin at `/admin/`.

Change the password anytime:

    "C:\Users\redee\anaconda3\python.exe" manage.py changepassword redeemertafadzwa@gmail.com

## Email confirmation codes
By default (no email configured) the 6-digit codes are printed to the **server
console** — copy them from there to confirm a new account while testing.

To send **real** emails, copy `.env.example` to `.env` and fill in:

    EMAIL_HOST_USER=your@gmail.com
    EMAIL_HOST_PASSWORD=your-16-char-app-password

For Gmail, generate an *App Password* (Google Account → Security → App
passwords). Restart the server after editing `.env`.

## Promo code
`NUST000` gives 20% off at the cart/checkout. Change it in `.env`:

    PROMO_CODE=NUST000
    PROMO_DISCOUNT_PERCENT=20

## Project layout
- `config/` — settings, root URLs
- `accounts/` — custom email user, verification codes, dashboard, user admin
- `store/` — categories, products, cart, orders, search logging
- `templates/`, `static/` — the bright editorial UI
- `store/management/commands/seed.py` — the starter catalogue

## Next step: hosting on Vercel
The project is Vercel-ready in structure (WhiteNoise static serving,
env-driven settings). Deploying Django to Vercel needs a serverless entry
point, a Postgres database (Vercel filesystem is read-only), and an email
provider — we'll wire that up together when you're ready.
