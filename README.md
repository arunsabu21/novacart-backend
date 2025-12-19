# NovaCart – Backend (v1)

NovaCart is a backend REST API for an e-commerce application, built using Django Rest Framework.  
The project follows an API-first approach and focuses on clean, scalable, production-style backend architecture.

## Live API
https://novacart-backend-bnnb.onrender.com

> Deployed on Render free tier (cold start may occur on first request)

---

## Tech Stack
- Python
- Django
- Django Rest Framework (DRF)
- JWT Authentication (SimpleJWT)
- Stripe (PaymentIntents + Webhooks)
- Postman (API Testing)
- SQLite (development / free-tier deployment)
- Render (Backend deployment)

---

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

---

## API Endpoints

### Authentication
- `POST /api/token/`
- `POST /api/token/refresh/`

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
- SQLite is used for learning and free-tier deployment purposes
- Data may reset on instance restart due to hosting limitations
- Backend is API-only; frontend consumes these endpoints
- JWT authentication is required for all protected routes
- Stripe secrets and webhook keys are managed via environment variables

---

## Author
**Arun**  
Software Developer

---

## Version
v1 – Core backend completed  
(Auth, Products, Wishlist, Cart, Orders, Payments, Webhooks, Order Cancellation)
