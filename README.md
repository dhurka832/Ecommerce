# Django E-Commerce Store

A simple E-Commerce web application built with Django featuring product browsing, cart management, wishlist functionality, user authentication, order tracking, and Stripe payment integration.

## Features

* User Registration & Login
* Product Search & Category Filtering
* Shopping Cart Management
* Wishlist Functionality
* Stripe Payment Gateway
* Order History
* Quantity Management
* Secure Authentication

## Tech Stack

* Django
* SQLite
* Stripe API
* HTML, CSS, Bootstrap

## Installation

```bash
git clone https://github.com/your-username/django-ecommerce-store.git
cd django-ecommerce-store

pip install -r requirements.txt
```

Create a `.env` file or update `settings.py`:

```env
STRIPE_SECRET_KEY=your_stripe_secret_key
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

## Usage

1. Register or login.
2. Browse products by category.
3. Add products to cart or wishlist.
4. Proceed to checkout using Stripe.
5. View order history after purchase.

## Features Overview

* Product Search
* Shopping Cart
* Wishlist
* Stripe Payments
* Order Management
* User Authentication

## Screenshots
