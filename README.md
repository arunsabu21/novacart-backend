# NovaCart – Backend (v1)

NovaCart is a backend REST API for an e-commerce application, built using Django Rest Framework.  
This project follows an API-first approach and focuses on clean, scalable backend architecture.

##  Live API
https://novacart-backend-bnnb.onrender.com

> Deployed on Render free tier (cold start may occur on first request)

---

##  Tech Stack
- Python
- Django
- Django Rest Framework (DRF)
- JWT Authentication (SimpleJWT)
- Postman (API Testing)
- SQLite (development / free-tier deployment)
- Render (Backend deployment)

---

##  Features (v1)
- User authentication using JWT
- Product listing and product detail APIs
- Wishlist functionality
- Cart functionality (Add / Update / Remove / Fetch)
- **Orders management (Cart → Order conversion)**
- Admin panel for managing data
- Password reset via email
- RESTful API design

---

##  API Endpoints

###  Authentication
- `POST /api/token/`
- `POST /api/token/refresh/`

---

###  Products
- `GET /api/products/`
- `POST /api/products/`
- `GET /api/products/<id>/`
- `PUT /api/products/<id>/`
- `DELETE /api/products/<id>/`

---

###  Wishlist
- `POST /api/products/wishlist/`
- `GET /api/products/wishlist/`
- `DELETE /api/products/wishlist/<id>/`

---

###  Cart
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

###  Orders
> All order endpoints require JWT authentication

- `POST /api/orders/create/`  
  Create an order from cart items (clears cart after success)

- `GET /api/orders/my/`  
  Fetch logged-in user’s order history

---

##  Project Status
This project is under active development.

### Planned Features
- Checkout flow
- Payment integration (Razorpay / Stripe)
- Frontend UI (React)
- Persistent production database (PostgreSQL)
- Deployment hardening (DEBUG=False, env-based config)

---

##  Notes
- SQLite is used for learning and free-tier deployment purposes
- Data may reset on instance restart due to hosting limitations
- Backend is API-only; frontend consumes these endpoints
- JWT authentication is required for protected routes

---

##  Author
**Arun**  
Software Developer

---

##  Version
v1 – Core backend features completed  
(Auth, Products, Wishlist, Cart, Orders)
