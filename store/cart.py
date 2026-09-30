from decimal import Decimal

from django.conf import settings

from .models import Product

CART_SESSION_KEY = "cart"
PROMO_SESSION_KEY = "promo"


class Cart:
    """A session-backed shopping cart. Keys are product ids, values hold qty."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def add(self, product, quantity=1, replace=False):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {"quantity": 0}
        if replace:
            self.cart[pid]["quantity"] = quantity
        else:
            self.cart[pid]["quantity"] += quantity
        if self.cart[pid]["quantity"] < 1:
            self.remove(product)
        else:
            self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.session.pop(PROMO_SESSION_KEY, None)
        self.session.modified = True

    def _products(self):
        ids = self.cart.keys()
        return Product.objects.filter(id__in=ids)

    def __iter__(self):
        products = {str(p.id): p for p in self._products()}
        for pid, item in self.cart.items():
            product = products.get(pid)
            if not product:
                continue
            qty = item["quantity"]
            yield {
                "product": product,
                "quantity": qty,
                "line_total": product.price * qty,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    @property
    def subtotal(self):
        return sum(
            (row["line_total"] for row in self), Decimal("0.00")
        )

    # ---- promo handling ----
    @property
    def promo_code(self):
        return self.session.get(PROMO_SESSION_KEY, "")

    def apply_promo(self, code):
        code = (code or "").strip().upper()
        if code == settings.PROMO_CODE.upper():
            self.session[PROMO_SESSION_KEY] = code
            self.session.modified = True
            return True
        return False

    def clear_promo(self):
        self.session.pop(PROMO_SESSION_KEY, None)
        self.session.modified = True

    @property
    def discount(self):
        if self.promo_code and self.promo_code.upper() == settings.PROMO_CODE.upper():
            pct = Decimal(settings.PROMO_DISCOUNT_PERCENT) / Decimal(100)
            return (self.subtotal * pct).quantize(Decimal("0.01"))
        return Decimal("0.00")

    @property
    def total(self):
        return (self.subtotal - self.discount).quantize(Decimal("0.01"))
