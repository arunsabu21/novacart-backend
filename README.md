# NovaCart Backend

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Django](https://img.shields.io/badge/django-5.0+-darkgreen.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

A production-ready REST API for a modern e-commerce platform built with Django and Django REST Framework. Features include authentication, product management, shopping cart, order processing, and Stripe payment integration.

[Live Demo](https://novacart-backend-bnnb.onrender.com) • [Report Bug](https://github.com/arunsabu21/novacart-backend/issues) • [Request Feature](https://github.com/arunsabu21/novacart-backend/issues)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Order Lifecycle](#order-lifecycle)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

NovaCart Backend is an API-first e-commerce platform that provides a complete suite of features for building modern online shopping experiences. The API follows RESTful principles and implements industry-standard patterns for authentication, payment processing, and order management.


[https://novacart-backend-staging.onrender.com](https://novacart-backend-staging.onrender.com)

(Hosted on Render — first request may have a cold start.)
=======
**Key Highlights:**
- JWT-based authentication with access/refresh tokens
- Stripe payment integration with webhook support
- Real-time cart management
- Complete order lifecycle management
- Cloud-ready with Cloudinary media storage
- Email notifications via Resend
- Production-deployed on Render


---

## Live Demo

**API Base URL:** [https://novacart-backend-bnnb.onrender.com](https://novacart-backend-staging.onrender.com)

⚠️ **Note:** Hosted on Render's free tier. First request may experience a cold start (30-60 seconds). Data may reset periodically.

**Test the API:**
```bash
# Get all products
curl https://novacart-backend-bnnb.onrender.com/api/products/

# Health check
curl https://novacart-backend-bnnb.onrender.com/api/health/
```

---

## Tech Stack

### Core Framework
- **Python** 3.10+
- **Django** 5.0+
- **Django REST Framework** 3.14+

### Authentication & Security
- **SimpleJWT** - JWT token authentication
- **Django CORS Headers** - Cross-origin resource sharing

### Database
- **PostgreSQL** - Production database (Neon Serverless)
- **SQLite** - Local development

### Payment Processing
- **Stripe** - Payment gateway and webhooks

### External Services
- **Cloudinary** - CDN and image hosting
- **Resend** - Transactional email service

### DevOps & Deployment
- **Render** - Platform as a Service
- **GitHub Actions** - CI/CD pipeline
- **Gunicorn** - WSGI HTTP server
- **WhiteNoise** - Static file serving

---

## Features

### Implemented

- **Authentication**
  - User registration and login
  - JWT access and refresh tokens
  - Password reset via email
  - Token expiration handling

- **Product Management**
  - CRUD operations for products
  - Product image uploads (Cloudinary)
  - Product search and filtering
  - Admin-only product creation/editing

- **Wishlist**
  - Add/remove products from wishlist
  - View user wishlist
  - Wishlist persistence

- **Shopping Cart**
  - Add items to cart
  - Update item quantities
  - Remove items from cart
  - Cart totals calculation
  - User-specific cart management

- **Order Management**
  - Create orders from cart
  - View order history
  - Cancel pending orders
  - Order status tracking
  - Admin order management

- **Payment Integration**
  - Stripe PaymentIntent creation
  - Secure webhook handling
  - Payment confirmation
  - Order status updates

- **Address Management**
  - Multiple addresses per user
  - Address types (HOME/OFFICE)
  - Default address selection

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.10 or higher
- **pip** (Python package manager)
- **Git**
- **PostgreSQL** 13+ (for production)

**External Accounts Required:**
- [Stripe Account](https://stripe.com) - Payment processing
- [Cloudinary Account](https://cloudinary.com) - Media storage
- [Resend Account](https://resend.com) - Email service
- [Neon Account](https://neon.tech) (optional) - PostgreSQL hosting

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/arunsabu21/novacart-backend.git
cd novacart-backend
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration (see [Environment Variables](#environment-variables) section).

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Load Sample Data (Optional)

```bash
python manage.py loaddata fixtures/sample_products.json
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

### Django Core (Required)

```env
# Django Secret Key
# Generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=your-secret-key-here

# Debug Mode (NEVER set to True in production)
DEBUG=True

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com
```

### Database (Required for Production)

```env
# PostgreSQL Configuration
POSTGRES_DB=novacart_db
POSTGRES_USER=novacart_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=your-db-host.neon.tech
POSTGRES_PORT=5432

# Database URL (alternative format)
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### Email Service (Required)

```env
# Resend Configuration
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=re_your_api_key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Stripe (Required)

```env
# Stripe API Keys
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key

# Stripe Webhook Secret
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### Cloudinary (Required)

```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Optional Settings

```env
# JWT Token Lifetimes (in minutes)
ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=10080  # 7 days

# CORS Settings (for frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

⚠️ **Security Warning:** Never commit `.env` files to version control. Add `.env` to your `.gitignore`.

---

## Project Structure

```
novacart-backend/
│
├── backend/                    # Django project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI entry point
│
├── users/                      # User authentication app
│   ├── models.py              # Custom user model
│   ├── serializers.py         # User serializers
│   ├── views.py               # Auth views
│   └── urls.py                # Auth endpoints
│
├── products/                   # Product catalog app
│   ├── models.py              # Product, Category, Wishlist
│   ├── serializers.py         # Product serializers
│   ├── views.py               # Product CRUD views
│   └── urls.py                # Product endpoints
│
├── cart/                       # Shopping cart app
│   ├── models.py              # Cart, CartItem models
│   ├── serializers.py         # Cart serializers
│   ├── views.py               # Cart operations
│   └── urls.py                # Cart endpoints
│
├── orders/                     # Order management app
│   ├── models.py              # Order, OrderItem models
│   ├── serializers.py         # Order serializers
│   ├── views.py               # Order lifecycle views
│   └── urls.py                # Order endpoints
│
├── payments/                   # Payment integration app
│   ├── views.py               # Stripe integration
│   ├── webhooks.py            # Webhook handlers
│   └── urls.py                # Payment endpoints
│
├── addresses/                  # Address management app
│   ├── models.py              # Address model
│   ├── serializers.py         # Address serializers
│   └── views.py               # Address CRUD
│
├── media/                      # User-uploaded files
├── staticfiles/                # Collected static files
├── fixtures/                   # Sample data
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## Architecture

### Design Pattern

NovaCart follows a **Modular Monolith** architecture with an **API-first** approach using Django REST Framework.

### Architectural Principles

- **RESTful API Design** - Stateless, resource-based endpoints
- **Stateless Authentication** - JWT tokens for scalability
- **App-Based Modularity** - Each Django app handles a specific domain
- **Server-Side Validation** - Business rules enforced at the backend
- **Separation of Concerns** - Clear boundaries between apps

### App Responsibilities

| App | Responsibility |
|-----|----------------|
| `users` | Authentication, JWT handling, user profiles |
| `products` | Product catalog, images, categories, wishlist |
| `cart` | Cart state management, quantity updates |
| `orders` | Order creation, lifecycle, cancellation |
| `payments` | Stripe PaymentIntent, webhook verification |
| `addresses` | User addresses, default address logic |

### Data Flow Example (Order Creation)

```
1. Client → POST /api/orders/create/
2. Backend validates user cart
3. Order created with status=PENDING
4. Stripe PaymentIntent generated
5. Client completes payment
6. Stripe webhook → /api/payments/webhook/
7. Backend updates order status=PAID
8. Cart items cleared
```

### Key Design Decisions

- **Thin Views, Strong Serializers** - Business logic in serializers
- **Service Layer Pattern** - Complex operations in dedicated services
- **Webhook-Driven Updates** - Stripe webhooks ensure consistency
- **Token-Based Auth** - Scalable authentication for mobile/web

---

## API Documentation

### Base URL

```
Production: https://novacart-backend-bnnb.onrender.com
Local: http://127.0.0.1:8000
```

### Authentication

All authenticated endpoints require a JWT access token in the header:

```http
Authorization: Bearer <your_access_token>
```

#### Token Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/token/` | Obtain access & refresh tokens | No |
| POST | `/api/token/refresh/` | Refresh access token | No |
| POST | `/api/token/verify/` | Verify token validity | No |

**Example: Obtain Token**

```bash
curl -X POST https://novacart-backend-bnnb.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Token Lifetimes:**
- Access Token: 60 minutes
- Refresh Token: 7 days

---

### Products

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List all products | No |
| POST | `/api/products/` | Create product | Yes (Admin) |
| GET | `/api/products/<id>/` | Get product details | No |
| PUT | `/api/products/<id>/` | Update product | Yes (Admin) |
| PATCH | `/api/products/<id>/` | Partial update | Yes (Admin) |
| DELETE | `/api/products/<id>/` | Delete product | Yes (Admin) |

**Example: List Products**

```bash
curl https://novacart-backend-bnnb.onrender.com/api/products/
```

---

### Wishlist

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/wishlist/` | Get user wishlist | Yes |
| POST | `/api/products/wishlist/` | Add to wishlist | Yes |
| DELETE | `/api/products/wishlist/<id>/` | Remove from wishlist | Yes |

**Example: Add to Wishlist**

```bash
curl -X POST https://novacart-backend-bnnb.onrender.com/api/products/wishlist/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'
```

---

### Cart

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cart/` | View cart | Yes |
| POST | `/api/cart/add/` | Add item to cart | Yes |
| PATCH | `/api/cart/update/<cart_id>/` | Update quantity | Yes |
| DELETE | `/api/cart/remove/<cart_id>/` | Remove item | Yes |
| DELETE | `/api/cart/clear/` | Clear entire cart | Yes |

**Example: Add to Cart**

```bash
curl -X POST https://novacart-backend-bnnb.onrender.com/api/cart/add/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

---

### Orders

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/my/` | Get user orders | Yes |
| POST | `/api/orders/create/` | Create order from cart | Yes |
| GET | `/api/orders/<id>/` | Get order details | Yes |
| POST | `/api/orders/cancel/<id>/` | Cancel order | Yes |

**Example: Create Order**

```bash
curl -X POST https://novacart-backend-bnnb.onrender.com/api/orders/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address_id": 1,
    "payment_method": "card"
  }'
```

---

### Payments

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/payments/payment-intent/` | Create Stripe PaymentIntent | Yes |
| POST | `/api/payments/webhook/` | Stripe webhook endpoint | No (Signed) |

**Example: Create Payment Intent**

```bash
curl -X POST https://novacart-backend-bnnb.onrender.com/api/payments/payment-intent/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 123,
    "amount": 5999
  }'
```

---

### Addresses

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/addresses/` | List user addresses | Yes |
| POST | `/api/addresses/` | Create address | Yes |
| PUT | `/api/addresses/<id>/` | Update address | Yes |
| DELETE | `/api/addresses/<id>/` | Delete address | Yes |
| POST | `/api/addresses/<id>/set-default/` | Set as default | Yes |

---

## Order Lifecycle

### Order States

```
PENDING → PAID → SHIPPED → DELIVERED
   ↓
CANCELLED
```

| Status | Description | User Actions |
|--------|-------------|--------------|
| `PENDING` | Order created, awaiting payment | Can cancel |
| `PAID` | Payment confirmed via webhook | View details |
| `SHIPPED` | Order dispatched | Track shipment |
| `DELIVERED` | Order completed | None |
| `CANCELLED` | Order cancelled before payment | None |

### State Transitions

1. **Order Creation** (`PENDING`)
   - User creates order from cart
   - Cart items locked
   - Stripe PaymentIntent created

2. **Payment Confirmation** (`PAID`)
   - Stripe webhook received
   - Order status updated
   - Cart cleared
   - Confirmation email sent

3. **Shipping** (`SHIPPED`)
   - Admin marks as shipped
   - Tracking info added
   - Shipping notification sent

4. **Delivery** (`DELIVERED`)
   - Admin confirms delivery
   - Order marked complete

5. **Cancellation** (`CANCELLED`)
   - Only possible in `PENDING` state
   - Cart items restored
   - Cancellation email sent

---

## Testing

### Run All Tests

```bash
python manage.py test
```

### Run Specific App Tests

```bash
python manage.py test users
python manage.py test products
python manage.py test orders
```

### Test Coverage

Install coverage:

```bash
pip install coverage
```

Generate coverage report:

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

View HTML report:

```bash
open htmlcov/index.html
```

### Test Data

Load test fixtures:

```bash
python manage.py loaddata fixtures/test_data.json
```

---

## Deployment

### Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure production `ALLOWED_HOSTS`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set strong `SECRET_KEY`
- [ ] Configure Cloudinary for media
- [ ] Set up Stripe webhook endpoint
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`
- [ ] Set up SSL/TLS certificate
- [ ] Configure CORS for frontend domain
- [ ] Set up error monitoring (Sentry)
- [ ] Configure backup strategy
- [ ] Enable rate limiting

### Deploy to Render

1. **Create PostgreSQL Database**
   - Go to Render Dashboard
   - Create new PostgreSQL instance
   - Copy internal database URL

2. **Create Web Service**
   - Connect GitHub repository
   - Set environment variables
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn backend.wsgi:application`

3. **Configure Environment Variables**

```env
DEBUG=False
SECRET_KEY=<production-secret>
DATABASE_URL=<render-postgres-url>
ALLOWED_HOSTS=.onrender.com
STRIPE_SECRET_KEY=<production-stripe-key>
STRIPE_WEBHOOK_SECRET=<webhook-secret>
```

4. **Set Up Stripe Webhooks**
   - Go to Stripe Dashboard → Webhooks
   - Add endpoint: `https://your-app.onrender.com/api/payments/webhook/`
   - Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`
   - Copy webhook secret to environment

5. **Deploy**
   - Push to GitHub
   - Render auto-deploys
   - Run migrations: `python manage.py migrate`

### Manual Deployment (VPS)

```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start with Gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## Security

### Authentication & Authorization

- **JWT Tokens**: All authenticated endpoints use JWT
- **Token Expiration**: Access tokens expire in 60 minutes
- **Refresh Tokens**: Secure refresh mechanism (7-day expiry)
- **Password Hashing**: Django's PBKDF2 algorithm

### Payment Security

- **Stripe Integration**: PCI-compliant payment processing
- **Webhook Verification**: All webhooks verify Stripe signatures
- **No Card Storage**: Card details never touch our servers

### Data Protection

- **SQL Injection**: Protected via Django ORM
- **XSS Prevention**: DRF automatic escaping
- **CSRF Protection**: Token-based protection
- **CORS**: Configured for specific origins only

### Production Settings

```python
# settings.py (production)
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

### Rate Limiting

Consider implementing rate limiting for production:

```bash
pip install django-ratelimit
```

---

## Troubleshooting

### Common Issues

#### 1. Cold Start on Render

**Problem:** First request takes 30-60 seconds

**Solution:** This is normal for Render's free tier.

## Author
Arun Sabu (Software Engineer) </br>
GitHub: [@arunsabu21](https://github.com/arunsabu21) </br>
Linkedin: [@arunsabu21](https://linkedin.com/in/arunsabu21)
