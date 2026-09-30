from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Order, OrderItem, Product, SearchLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "emoji", "order", "product_count")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumb", "name", "category", "price", "in_stock",
        "is_featured", "purchase_count", "search_count",
    )
    list_display_links = ("thumb", "name")
    list_editable = ("in_stock", "is_featured")
    list_filter = ("category", "in_stock", "is_featured")
    search_fields = ("name", "description", "color")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("search_count", "purchase_count", "created_at")

    @admin.display(description="")
    def thumb(self, obj):
        if obj.display_image:
            return format_html(
                '<img src="{}" style="width:44px;height:56px;object-fit:cover;border-radius:6px">',
                obj.display_image,
            )
        return "—"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "name", "price", "quantity", "line_total")

    @admin.display(description="Line total")
    def line_total(self, obj):
        return obj.line_total


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "total", "promo_code", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "id")
    readonly_fields = ("subtotal", "discount", "total", "promo_code", "created_at")
    inlines = [OrderItemInline]


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "results", "created_at")
    search_fields = ("query",)
    list_filter = ("created_at",)
