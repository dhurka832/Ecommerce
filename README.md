# LUXE Store — Django E-Commerce

A full-featured Django e-commerce web application with a modern UI. Supports product browsing, cart management, wishlists, user authentication, order tracking, and Stripe payment integration.

---

## Features

- User registration and login
- Product search and category filtering
- Shopping cart with quantity management
- Wishlist functionality
- Stripe payment gateway (test mode ready)
- Order history tracking
- Responsive design — works on mobile and desktop
- Sticky navbar with live search
- Toast notifications for cart/wishlist actions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x |
| Database | SQLite |
| Payments | Stripe API |
| Frontend | HTML, CSS (custom), Font Awesome, Google Fonts |
| Forms | django-crispy-forms + crispy-bootstrap5 |
| Auth | Django built-in authentication |

---

## Project Structure

```
project/
├── manage.py
├── db.sqlite3
├── .env
├── ecommerce/
│   ├── __init__.py
│   ├── settings.py
│   └── urls.py
└── store/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── apps.py
    └── templates/store/
        ├── base.html          # Shared layout, navbar, footer
        ├── home.html          # Product grid, hero, category filter
        ├── product_detail.html
        ├── cart.html
        ├── wishlist.html
        ├── checkout.html      # Stripe card element
        ├── order_success.html
        ├── order_history.html
        ├── login.html
        └── register.html
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/dhurka832/django-ecommerce-store.git
cd django-ecommerce-store
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate        # macOS / Linux
env\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install django python-dotenv stripe django-crispy-forms crispy-bootstrap5 Pillow
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
```

Get your keys from [https://dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys).

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000)

---

## Database Models

| Model | Fields |
|---|---|
| `Category` | name |
| `Product` | name, price, description, image, category |
| `Cart` | user, created_at |
| `CartItem` | cart, product, quantity |
| `Order` | user, total_price, created_at, status |
| `OrderItem` | order, product, quantity |
| `Wishlist` | user, product |

---

## Usage

1. Register or log in at `/register/` or `/login/`
2. Browse products on the home page — filter by category or search
3. Click a product to view its detail page
4. Add products to your cart or wishlist
5. Go to `/cart/` and proceed to checkout
6. Pay using Stripe (test card: `4242 4242 4242 4242`, any future date, any CVC)
7. View your order history at `/orders/`

---

## URL Reference

| URL | View | Description |
|---|---|---|
| `/` | `home` | Product listing with search and filter |
| `/product/<id>/` | `product_detail` | Single product page |
| `/cart/` | `cart` | Shopping cart |
| `/add-to-cart/<id>/` | `add_to_cart` | Add item to cart |
| `/remove-from-cart/<id>/` | `remove_from_cart` | Remove item from cart |
| `/update-cart/<id>/` | `update_cart` | Update item quantity |
| `/wishlist/` | `wishlist` | Saved items |
| `/add-to-wishlist/<id>/` | `add_to_wishlist` | Save item to wishlist |
| `/remove-from-wishlist/<id>/` | `remove_from_wishlist` | Remove from wishlist |
| `/checkout/` | `checkout` | Stripe payment form |
| `/order-success/` | `order_success` | Confirmation page |
| `/orders/` | `order_history` | Past orders |
| `/register/` | `register` | New user signup |
| `/login/` | `login` | Login |
| `/logout/` | `logout` | Logout |
| `/admin/` | Django admin | Admin panel |

---

## Stripe Test Cards

| Card Number | Scenario |
|---|---|
| `4242 4242 4242 4242` | Payment succeeds |
| `4000 0000 0000 0002` | Payment declined |
| `4000 0025 0000 3155` | Requires authentication |

Use any future expiry date and any 3-digit CVC.

---

## Admin Panel

Access the Django admin at `/admin/` to manage products, categories, orders, and users. Create a superuser first with `python manage.py createsuperuser`.

---