from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .forms import CheckoutForm
from .models import Category, Order, OrderItem, Product, SearchLog

SORTS = {
    "new": "-created_at",
    "price_low": "price",
    "price_high": "-price",
    "name": "name",
}


def home(request):
    featured = Product.objects.filter(is_featured=True, in_stock=True)[:8]
    if not featured.exists():
        featured = Product.objects.filter(in_stock=True)[:8]
    new_arrivals = Product.objects.filter(in_stock=True).order_by("-created_at")[:8]
    trending = Product.objects.filter(purchase_count__gt=0).order_by("-purchase_count")[:8]
    return render(request, "store/home.html", {
        "featured": featured,
        "new_arrivals": new_arrivals,
        "trending": trending,
        "categories": Category.objects.all(),
    })


def catalog(request):
    products = Product.objects.select_related("category").all()

    query = request.GET.get("q", "").strip()
    cat_slug = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "new")
    active_category = None

    if cat_slug:
        active_category = Category.objects.filter(slug=cat_slug).first()
        if active_category:
            products = products.filter(category=active_category)

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(color__icontains=query)
        ).distinct()

    products = products.order_by(SORTS.get(sort, "-created_at"))

    # Log the search so it feeds the dashboard analytics.
    if query:
        SearchLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            query=query,
            results=products.count(),
        )

    return render(request, "store/catalog.html", {
        "products": products,
        "query": query,
        "active_category": active_category,
        "sort": sort,
        "categories": Category.objects.all(),
        "sort_options": [
            ("new", "Newest"),
            ("price_low", "Price: low to high"),
            ("price_high", "Price: high to low"),
            ("name", "Name A-Z"),
        ],
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    # Count interest so trending / most-searched has data to show.
    Product.objects.filter(pk=product.pk).update(search_count=product.search_count + 1)
    related = (
        Product.objects.filter(category=product.category, in_stock=True)
        .exclude(pk=product.pk)[:4]
    )
    return render(request, "store/product_detail.html", {
        "product": product,
        "related": related,
    })


def cart_add(request, product_id):
    if request.method != "POST":
        return redirect("store:cart")
    product = get_object_or_404(Product, id=product_id)
    try:
        qty = max(1, int(request.POST.get("quantity", 1)))
    except (TypeError, ValueError):
        qty = 1
    cart = Cart(request)
    cart.add(product, quantity=qty)
    messages.success(request, f"Added “{product.name}” to your cart.")
    if request.POST.get("next") == "cart":
        return redirect("store:cart")
    return redirect(product.get_absolute_url())


def cart_view(request):
    cart = Cart(request)
    return render(request, "store/cart.html", {
        "cart": cart,
        "promo_code_hint": settings.PROMO_CODE,
    })


def cart_update(request, product_id):
    if request.method != "POST":
        return redirect("store:cart")
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1
    cart.add(product, quantity=qty, replace=True)
    return redirect("store:cart")


def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove(product)
    messages.info(request, f"Removed “{product.name}” from your cart.")
    return redirect("store:cart")


def apply_promo(request):
    if request.method == "POST":
        cart = Cart(request)
        code = request.POST.get("promo", "")
        if cart.apply_promo(code):
            messages.success(
                request,
                f"Promo code applied - {settings.PROMO_DISCOUNT_PERCENT}% off your order!",
            )
        else:
            messages.error(request, "That promo code isn't valid.")
    return redirect(request.POST.get("next", "store:cart"))


def remove_promo(request):
    Cart(request).clear_promo()
    messages.info(request, "Promo code removed.")
    return redirect("store:cart")


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty - add something first.")
        return redirect("store:catalog")

    initial = {}
    if request.user.is_authenticated:
        initial = {"full_name": request.user.display_name, "email": request.user.email}

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.subtotal = cart.subtotal
            order.discount = cart.discount
            order.total = cart.total
            order.promo_code = cart.promo_code
            order.save()

            for row in cart:
                product = row["product"]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    name=product.name,
                    price=product.price,
                    quantity=row["quantity"],
                )
                Product.objects.filter(pk=product.pk).update(
                    purchase_count=product.purchase_count + row["quantity"]
                )

            cart.clear()
            messages.success(request, "Order placed! Thank you for shopping with DK Fashions.")
            return redirect("store:order_success", order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "store/checkout.html", {
        "cart": cart,
        "form": form,
        "promo_code_hint": settings.PROMO_CODE,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "store/order_success.html", {"order": order})
