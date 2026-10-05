# 🛍️ LUXE — Full-Stack E-Commerce & AI Concierge

A modern, high-performance e-commerce web platform built with **Django 5** and **Pure HTML5 / CSS3 / Vanilla JavaScript** (Zero Bootstrap), featuring an interactive **AI Support Concierge**, dynamic bento-grid catalog, and secure **Stripe Payment API** integration.

---

## ⚡ Key Highlights

- **Bespoke Card-Driven UI:** Handcrafted design system built with pure CSS & vanilla JS, featuring bento grids, responsive mobile drawers, and smooth micro-interactions.
- **AI Concierge Assistant:** Real-time conversational support widget for instant FAQ resolution, order tracking, and product recommendations.
- **Secure Stripe Checkout:** End-to-end payment gateway integration with live interactive credit card formatting and instant test simulator presets.
- **Complete Shopping Lifecycle:** User authentication, dynamic category filtering, live search, cart quantity steppers, wishlist persistence, and order history tracking.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Django 5.x, SQLite / Django ORM
- **Payments:** Stripe API (Test & Live Card Support)
- **Frontend:** HTML5, Modern CSS3 (Flexbox/Grid, Custom Properties), Vanilla JavaScript (ES6+)
- **Icons & Typography:** Font Awesome 6, Google Fonts (Syne, Plus Jakarta Sans)

---

## 🚀 Quick Start

### 1. Clone & Activate Virtual Environment
```bash
git clone https://github.com/dhurka832/django-ecommerce-store.git
cd django-ecommerce-store
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
```

### 4. Migrate & Launch
```bash
python manage.py migrate
python manage.py runserver
```
Visit `http://localhost:8000` in your browser.

---

## 📁 Project Architecture

```text
Ecommerce/
├── ecommerce/          # Django project settings & root routing
├── store/              # Main commerce application
│   ├── static/store/   # Bespoke CSS, vanilla JS & chatbot engine
│   ├── templates/store/# Custom HTML5 card-driven templates
│   ├── models.py       # Product, Cart, Order, Wishlist schemas
│   └── views.py        # Business logic & AI chatbot API endpoint
└── manage.py
```

---

## 📄 License
MIT License © 2026 LUXE Studio.