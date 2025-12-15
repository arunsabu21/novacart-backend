# NovaCart – Backend (v1)

NovaCart is a backend REST API for an e-commerce application, built using Django Rest Framework.  
This project focuses on core backend functionality and follows an API-first approach.

##  Live API
https://novacart-backend-bnnb.onrender.com

> Deployed on Render free tier (cold start may occur on first request)

---

##  Tech Stack
- Python
- Django
- Django Rest Framework (DRF)
- JWT Authentication (SimpleJWT)
- SQLite (development / free-tier deployment)
- Render (Backend deployment)

---

##  Features (v1)
- User authentication using JWT
- Product listing and product detail APIs
- Wishlist functionality
- Admin panel for managing data
- Password reset via email
- RESTful API design

---

##  API Endpoints

### Authentication
- `POST /api/token/`
- `POST /api/token/refresh/`

### Products
- `GET /api/products/`
- `POST /api/products/`
- `GET /api/products/<id>/`
- `PUT /api/products/<id>/`
- `DELETE /api/products/<id>/`

### Wishlist
- `POST /api/products/wishlist/`
- `GET /api/products/wishlist/`
- `DELETE /api/products/wishlist/<id>/`

---

##  Project Status
This project is under active development.

Planned features:
- Cart functionality
- Orders management
- Payment integration
- UI and frontend enhancements
- Persistent production database (PostgreSQL)

---

## ⚠️ Notes
- SQLite is used for learning and free-tier deployment purposes
- Data may reset on instance restart due to hosting limitations
- Backend is API-only; frontend will consume these endpoints

---

## 👤 Author
**Arun**  
Software Developer

---

## 📌 Version
v1 – Initial production release
