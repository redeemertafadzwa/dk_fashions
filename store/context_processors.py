from django.conf import settings

from .cart import Cart
from .models import Category


def store_globals(request):
    """Nav categories, live cart count, and the promo code on every page."""
    cart = Cart(request)
    return {
        "nav_categories": Category.objects.all(),
        "cart_count": len(cart),
        "PROMO_CODE": settings.PROMO_CODE,
        "PROMO_DISCOUNT_PERCENT": settings.PROMO_DISCOUNT_PERCENT,
    }
