import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
import stripe
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Wishlist

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            msg = data.get('message', '').strip().lower()
        except Exception:
            msg = request.POST.get('message', '').strip().lower()

        if not msg:
            return JsonResponse({'reply': 'Hello! How can I assist you with your LUXE Store shopping today?'})

        if 'return' in msg or 'refund' in msg or 'exchange' in msg or 'policy' in msg and 'return' in msg:
            reply = "🤖 You can return eligible products within 7 days of delivery for a full refund or exchange. Items must be unused and in original packaging."

        elif 'shipping' in msg or 'delivery' in msg or 'dispatch' in msg or 'ship' in msg:
            reply = "🚚 We offer free standard shipping on all orders above ₹999! Standard delivery arrives within 2 to 4 business days."

        elif 'store' in msg or 'about' in msg or 'location' in msg or 'contact' in msg or 'hours' in msg or 'who are you' in msg:
            reply = "🏪 **LUXE Store** is a premier online shopping platform offering curated fashion, accessories, and electronics with 24/7 customer service."

        elif 'payment' in msg or 'pay' in msg or 'card' in msg or 'stripe' in msg or 'credit' in msg or 'debit' in msg:
            reply = "💳 We support all major Credit and Debit cards processed securely through Stripe API. All transactions are 100% encrypted."

        elif 'order' in msg or 'track' in msg or 'history' in msg or 'status' in msg:
            reply = "📦 You can view and track your order status anytime by clicking the 'Orders' link in the top navigation bar."

        elif 'product' in msg or 'item' in msg or 'catalog' in msg or 'stock' in msg or 'price' in msg:
            products = Product.objects.all()[:4]
            names = ", ".join([f"{p.name} (₹{p.price:.0f})" for p in products])
            reply = f"🛍️ Explore our featured products: {names}. Use the top search bar or category filters to browse!"

        else:
            matching = Product.objects.filter(name__icontains=msg)[:3]
            if matching.exists():
                items = ", ".join([f"**{p.name}** (₹{p.price:.0f})" for p in matching])
                reply = f"🔍 I found these matching items in our store: {items}. Search above to view full details!"
            else:
                reply = "👋 Hi! I am your LUXE AI Assistant. Ask me about Shipping, Returns, Payments, Order tracking, Store information, or product recommendations."

        return JsonResponse({'reply': reply})

    return JsonResponse({'error': 'POST method required'}, status=405)


def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products, 'categories': categories,
        'query': query, 'selected_category': category_id
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart_obj)
    total = sum(i.product.price * i.quantity for i in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def update_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('cart')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f'"{product.name}" added to wishlist!')
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, pk):
    item = get_object_or_404(Wishlist, pk=pk, user=request.user)
    item.delete()
    return redirect('wishlist')

@login_required
def checkout(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart_obj)
    total = sum(i.product.price * i.quantity for i in items)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '')
        TEST_CARD_TOKENS = {
            '4242424242424242': 'tok_visa',               # Success
            '4000000000000002': 'tok_chargeDeclined',      # Declined
            '4000000000009995': 'tok_chargeDeclinedInsufficientFunds',  # Insufficient funds
        }
        token = TEST_CARD_TOKENS.get(card_number)
        if not token:
            messages.error(request, 'Invalid test card number. Please use one of the test cards shown below.')
        else:
            try:
                stripe.Charge.create(amount=int(total * 100), currency='inr', source=token)
                order = Order.objects.create(user=request.user, total_price=total, status='Paid')
                for item in items:
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                items.delete()
                return redirect('order_success')
            except stripe.error.StripeError as e:
                messages.error(request, str(e))

    return render(request, 'store/checkout.html', {
        'items': items, 'total': total,
    })

@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control bg-light p-3'
        
    return render(request, 'store/register.html', {'form': form})
