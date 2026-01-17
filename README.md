# NovaCart — Backend (v1) 

A production-style REST API for an e-commerce application built with Django & Django REST Framework (DRF). The backend follows an API-first approach and implements real-world workflows including authentication, products, cart, orders, Stripe payments, and webhooks.

---

## Table of contents 

- [Live API](#live-api)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
- [Environment variables](#environment-variables)
- [Run locally](#run-locally)
- [Project structure](#project-structure)
- [Main features](#main-features)
- [API overview](#api-overview)
- [Order lifecycle](#order-lifecycle)
- [Deployment notes](#deployment-notes)
- [Author & License](#author--license)

---

## Live API 

The public demo is available at:

https://novacart-backend-bnnb.onrender.com

(Hosted on Render — first request may have a cold start.)

---

## Tech stack 

- Python 3.10+ (recommended)
- Django
- Django REST Framework
- Simple JWT for authentication
- Resend (email service)
- PostgreSQL (production database)
- SQLite (local testing)
- Stripe (payments & webhooks)
- Cloudinary (product images)
- Render (deployment)
- GitHub Actions (CI pipeline)

---

## Getting started 

Clone the repo and open the `backend/` folder to work on the API only.

```bash
git clone https://github.com/arunsabu21/novacart-backend.git
cd backend
```

Create and activate a virtual environment:

Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations and (optionally) create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Run the local development server:

```bash
python manage.py runserver
```

Run tests:

```bash
python manage.py test
```

---

## Environment variables 

Create a `.env` file in the `backend/` root and add (examples):

```env
# Django
SECRET_KEY=your_django_secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Postgres production example)
POSTGRES_DB=novacart
POSTGRES_USER=novacart_user
POSTGRES_PASSWORD=securepassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Email (Resend or SMTP)
EMAIL_HOST_USER=your@example.com
EMAIL_HOST_PASSWORD=email_password

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Cloudinary
CLOUDINARY_CLOUD_NAME=xxx
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx
```

 **Never** commit `.env` or other secrets into version control.

---

## Project structure 

Top-level folders in `backend/`:

- `backend/` — Django project settings
- `users/` — user model & auth
- `products/` — product models & APIs
- `cart/` — cart management
- `orders/` — order workflows
- `payments/` — Stripe integration & webhooks
- `media/`, `staticfiles/`
- `manage.py`, `requirements.txt`

Each app follows standard Django layout: `models`, `serializers`, `views`, `urls`, `migrations`.

---

## Backend Architecture

NovaCart follows a modular, API-first backend architecture using Django Rest Framework.

## Architectural Style

- RESTful APIs
- Stateless authentication using JWT
- App-based modular design
- Backend-enforced business rules

## App Responsibilities

- users — authentication, JWT handling, user management
- products — product catalog, images, wishlist
- cart — cart state & quantity management
- orders — order creation, cancellation, lifecycle
- payments — Stripe PaymentIntent & webhook verification
- addresses — user addresses (HOME / OFFICE, default address logic)

## Data Flow (Order Example)

1. Client creates order from cart
2. Backend validates cart items
3. Order created with PENDING status
4. Stripe PaymentIntent generated
5. Stripe webhook confirms payment
6. Order status updated to PAID

## Design Principles

- Thin views, strong serializers
- Business rules enforced server-side
- External services isolated per app
- Scalable structure for future growth


## Main features 

- JWT-based authentication
- Product listing & detail APIs
- Wishlist management
- Cart operations (add, remove, update qty, fetch)
- Order creation from cart, order history, cancel before payment
- Stripe PaymentIntent + webhook confirmation
- Admin dashboard for managing products, orders, users
- Password reset via email
- Media stored on Cloudinary (CDN-friendly)

---

## API overview 

Authentication
- `POST /api/token/` — obtain access & refresh tokens
- `POST /api/token/refresh/` — refresh access token

Products
- `GET /api/products/` — list products
- `POST /api/products/` — create product (admin)
- `GET /api/products/<id>/` — retrieve
- `PUT /api/products/<id>/` — update (admin)
- `DELETE /api/products/<id>/` — delete (admin)

Wishlist
- `POST /api/products/wishlist/`
- `GET /api/products/wishlist/`
- `DELETE /api/products/wishlist/<id>/`

Cart (authenticated)
- `POST /api/cart/add/` — add item
- `GET /api/cart/` — view cart
- `PATCH /api/cart/update/<cart_id>/` — update quantity
- `DELETE /api/cart/remove/<cart_id>/` — remove

Orders (authenticated)
- `POST /api/orders/create/` — create order from cart
- `GET /api/orders/my/` — user orders
- `POST /api/orders/cancel/<order_id>/` — cancel (pre-payment)

Payments
- `POST /api/payments/payment-intent/` — create Stripe PaymentIntent
- `POST /api/payments/webhook/` — Stripe webhook endpoint

Token lifetimes: Access token ~60 minutes; Refresh token ~7 days (configured via SimpleJWT).

---

## Order lifecycle 

- `PENDING` — created, awaiting payment
- `PAID` — payment confirmed via webhook
- `CANCELLED` — cancelled before payment

(Refund support is planned for future releases.)

---

## Future Improvements

- User address management
- Order invoice generation (PDF)
- Refund & return workflow
- Caching frequently accessed APIs (products, cart)

## Deployment notes 

- Production uses PostgreSQL and Cloudinary for persistent media.
- The public demo is hosted on Render; free-tier instances may sleep (cold start) and can reset data.
- Store all secrets in environment variables or a secrets manager.
- Consider adding monitoring and automated backups for production DB.

---

## Contributing & Support 

Contributions are welcome. Please open issues or PRs against the repository and follow standard GitHub contribution practices.

---

## Author & Version 

**Arun Sabu** — Backend Developer (Django / DRF)

**Version:** v1 — Core backend completed (Auth, Products, Wishlist, Cart, Orders, Payments, Webhooks).

---


