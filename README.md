# NovaCart – Backend (v1)

NovaCart is a backend REST API for an e-commerce application, built using Django Rest Framework.  
The project follows an API-first approach and focuses on clean, scalable, production-style backend architecture.

## Live API
https://novacart-backend-bnnb.onrender.com

> Deployed on Render free tier (cold start may occur on first request)

---

## Tech Stack
- Python 3
- Django
- Django Rest Framework (DRF)
- JWT Authentication (SimpleJWT)
- Stripe (PaymentIntents + Webhooks)
- Cloudinary – Media storage (Product images)
- SQLite (development / free-tier deployment)
- Render (Backend deployment)
- Postman (API Testing)

---

## Media Storage (Product Images)
Product images are stored in **Cloudinary**, not in local /media folder.

Benefits:
- CDN delivery (very fast globally)
- persists even when server sleeps
- ideal for Render free tier

Django uses:

- cloudinary
- django-cloudinary-storage

Images are uploaded through Django Admin.

## Environment Variables

Create a `.env` file in the backend root and add:

- SECRET_KEY=your_django_secret
- DEBUG=False
- ALLOWED_HOSTS=your-domain.com,localhost

### Email
- EMAIL_HOST_USER=your_email
- EMAIL_HOST_PASSWORD=your_email_password

### Stripe
- STRIPE_SECRET_KEY=your_key
- STRIPE_WEBHOOK_SECRET=your_key

### Cloudinary
- CLOUDINARY_CLOUD_NAME=xxx
- CLOUDINARY_API_KEY=xxx
- CLOUDINARY_API_SECRET=xxx

> Never commit `.env` to GitHub. It must stay private.

## How to Run Locally
1. Clone the Repo
```
git clone https://github.com/arunsabu21/novacart-backend.git
cd backend
```
2. Create virtual environment
```
python -m venv venv
```
3. Activate environment
```
Windows:

venv\Scripts\activate


Mac / Linux:

source venv/bin/activate
```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Apply migrations
```
python manage.py migrate
```
6. Run server
```
python manage.py runserver
```



## Project Structure
```
backend/
├── backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── products/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── cart/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── orders/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── payments/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── media/           # Local media (development) – Cloudinary used in production
├── staticfiles/     # Collected static files
├── manage.py
└── requirements.txt
```

## Features (v1)
- User authentication using JWT
- Product listing and product detail APIs
- Wishlist functionality
- Cart functionality (Add / Update / Remove / Fetch)
- Orders management (Cart → Order conversion)
- Secure payment processing using Stripe PaymentIntents
- Webhook-based asynchronous payment confirmation
- Order lifecycle management (PENDING → PAID → CANCELLED)
- Order cancellation (allowed only before payment)
- Admin panel for managing products, orders, and payments
- Password reset via email
- RESTful API design
- Cloudinary media storage for uploaded images

---

## API Endpoints

### Authentication
- `POST /api/token/`
- `POST /api/token/refresh/`
### Token Lifetime (Simple JWT)
- Access Token: 60 minutes
- Refresh Token: 7 days
> Configured in settings.py.

---

### Products
- `GET /api/products/`
- `POST /api/products/`
- `GET /api/products/<id>/`
- `PUT /api/products/<id>/`
- `DELETE /api/products/<id>/`

---

### Wishlist
- `POST /api/products/wishlist/`
- `GET /api/products/wishlist/`
- `DELETE /api/products/wishlist/<id>/`

---

### Cart  
> All cart endpoints require JWT authentication

- `POST /api/cart/add/`  
  Add a product to cart or increase quantity

- `GET /api/cart/`  
  Fetch logged-in user’s cart items

- `PATCH /api/cart/update/<cart_id>/`  
  Increase or decrease item quantity

- `DELETE /api/cart/remove/<cart_id>/`  
  Remove item from cart

---

### Orders  
> All order endpoints require JWT authentication

- `POST /api/orders/create/`  
  Create an order from cart items (clears cart after success)

- `GET /api/orders/my/`  
  Fetch logged-in user’s order history

- `POST /api/orders/cancel/<order_id>/`  
  Cancel an order (only allowed when status is PENDING)

---

### Payments  
> Payment confirmation handled asynchronously via Stripe webhooks

- `POST /api/payments/payment-intent/`  
  Create Stripe PaymentIntent for an order

- `POST /api/payments/webhook/`  
  Stripe webhook endpoint to confirm payment and update order status

---

## Order Lifecycle
- `PENDING` → Order created, payment not completed
- `PAID` → Payment confirmed via Stripe webhook
- `CANCELLED` → Order cancelled before payment

Paid orders cannot be cancelled. Refund functionality will be added in a future version.

---

## Project Status
This project is under active development.

### Planned Features
- Refund handling using Stripe Refund API
- Checkout UI (React)
- Persistent production database (PostgreSQL)
- Deployment hardening (DEBUG=False, env-based config)
- Enhanced order status tracking (Processing, Shipped, Delivered)

---

## Notes
- SQLite (development & free-tier deployment – switching to PostgreSQL soon)
- Data may reset on instance restart due to hosting limitations
- Backend is API-only; frontend consumes these endpoints
- JWT authentication is required for all protected routes
- Stripe secrets and webhook keys are managed via environment variables

---

## Author
**Arun Sabu**  
Backend Developer (Django / DRF)

---

## Version
v1 – Core backend completed  
(Auth, Products, Wishlist, Cart, Orders, Payments, Webhooks, Order Cancellation)
