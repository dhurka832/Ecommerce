## Ecommerce - LUXE Store

LUXE Store is a full-featured e-commerce web application built with Django. It features a modern, responsive user interface and provides all essential e-commerce functionalities, from product browsing and cart management to secure payments using Stripe.

### Features

- **User Authentication:** Registration, login, and secure user sessions.
- **Product Catalog:** Browse products, search functionality, and category filtering.
- **Shopping Cart:** Add/remove items and manage quantities seamlessly.
- **Wishlist:** Save favorite products for later.
- **Secure Checkout:** Integrated with Stripe API 
- **Order Management:** Track order history and status.
- **Responsive UI:** Works beautifully on both desktop and mobile devices, featuring a sticky navbar and toast notifications.

## Tech Stack

* **Backend:** Django 5.x, Python
* **Database:** SQLite 
* **Payments:** Stripe API 
* **Frontend:** HTML5, CSS3, Bootstrap 5 , Font Awesome, Google Fonts
* **Forms:** django-crispy-forms

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhurka832/django-ecommerce-store.git
   cd django-ecommerce-store
   ```

2. **Create and activate a virtual environment**
   * Windows:
     ```bash
     python -m venv env
     env\Scripts\activate
     ```
   * macOS / Linux:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root directory:
   ```env
   STRIPE_SECRET_KEY=sk_test_your_key_here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
   ```
   > Get your test keys from the [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys).

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://localhost:8000` in your browser.

## Stripe Test Cards

Use the following test cards in the Stripe checkout form (use any future expiry date and any 3-digit CVC):

| Scenario | Card Number |
| :--- | :--- |
| **Payment succeeds** | `4242 4242 4242 4242` |
| **Payment declined** | `4000 0000 0000 0002` |
| **Requires authentication** | `4000 0025 0000 3155` |

## Project Structure

```text
project/
├── manage.py
├── db.sqlite3
├── .env
├── requirements.txt
├── ecommerce/           
└── store/                
    ├── models.py        
    ├── views.py         
    ├── urls.py          
    └── templates/store/  
```

## Screenshots 

<p align="center">
  <img src="screenshots/main.jpg" alt="Main View" width="400"/>
  <img src="screenshots/all-products.jpg" alt="Product List View" width="400"/>
  <img src="screenshots/wishlist.jpg" alt="Wish List View" width="400"/>
  <img src="screenshots/cart.jpg" alt="Cart View" width="400"/>
  <img src="screenshots/checkout.jpg" alt="Checkout View" width="400"/>
  <img src="screenshots/order-success.jpg" alt="Order Success View" width="400"/>
  <img src="screenshots/orders.jpg" alt="Orders View" width="400"/>
  <img src="screenshots/register.jpg" alt="Register View" width="400"/>
  <img src="screenshots/login.jpg" alt="Login View" width="400"/>
</p>
