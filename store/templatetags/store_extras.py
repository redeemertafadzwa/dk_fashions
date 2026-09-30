from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Clean line-icons, 24x24, drawn with currentColor so they inherit text colour.
_PATHS = {
    # --- category icons ---
    "dresses": '<path d="M9 3l3 2 3-2"/><path d="M9 3c-.2 1.7-.7 2.8-1.6 3.6L12 9l4.6-2.4C15.7 5.8 15.2 4.7 15 3"/><path d="M8 6.5 5.6 19.2A1.5 1.5 0 0 0 7 21h10a1.5 1.5 0 0 0 1.4-1.8L16 6.5"/>',
    "tops-shirts": '<path d="M8.5 3 5 5.5l1.8 2.9L8.5 7.4V21h7V7.4l1.7 1L19 5.5 15.5 3a3.5 3.5 0 0 1-7 0Z"/>',
    "denim": '<path d="M6.8 3h10.4l.4 4H6.4l.4-4Z"/><path d="M6.4 7 8 21h2.2l1.4-9h.8l1.4 9H17l1.6-14"/><path d="M12 7v4"/>',
    "outerwear": '<path d="M12 3 8 4.5 4 7l1.7 3.2L8 9.3V21h8V9.3l2.3.9L20 7l-4-2.5L12 3Z"/><path d="M12 4.5 9.6 8H12m0-3.5L14.4 8H12m0 0v12"/>',
    "footwear": '<path d="M2.5 15.5h9l3.8-2 4.2 1.1c1.2.3 2 1.4 2 2.6v.8a1 1 0 0 1-1 1H1.9a.9.9 0 0 1-.9-.9v-1.7a.9.9 0 0 1 .9-.9Z"/><path d="M11.5 15.5 10.5 11l3.3 1.2"/><path d="M2.4 18h18.9"/>',
    "bags": '<path d="M5.5 8h13l-1 11.5a1.5 1.5 0 0 1-1.5 1.4H8a1.5 1.5 0 0 1-1.5-1.4L5.5 8Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
    "accessories": '<path d="M2.5 9.5 4 9h5l1.2 1.2M21.5 9.5 20 9h-5l-1.2 1.2"/><rect x="3.5" y="9.5" width="6.5" height="4.5" rx="2.2"/><rect x="14" y="9.5" width="6.5" height="4.5" rx="2.2"/><path d="M10 11.5h4"/>',
    "activewear": '<path d="M6.5 8v8M4 9.5v5M17.5 8v8M20 9.5v5M6.5 12h11"/>',
    # --- ui icons ---
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "flame": '<path d="M12 2.5c3 3.5 5 6 5 9.5a5 5 0 0 1-10 0c0-1.6.6-3 1.7-4.2.2 1 .8 1.8 1.6 2.2C11 8.6 10.5 6 12 2.5Z"/>',
    "bag": '<path d="M6 7h12l-1 13H7L6 7Z"/><path d="M9 7V5.5a3 3 0 0 1 6 0V7"/>',
    "box": '<path d="M12 2.5 20.5 7v10L12 21.5 3.5 17V7L12 2.5Z"/><path d="M3.5 7 12 11.5 20.5 7M12 11.5V21.5"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5.2l3.3 2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M4 7l8 5.5L20 7"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9.5"/>',
    "tag": '<path d="M3 12 12 3l8 .5.5 8L11.5 20.5a2 2 0 0 1-2.8 0L3 14.8a2 2 0 0 1 0-2.8Z"/><circle cx="15.5" cy="8.5" r="1.3"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
}

_ALIASES = {
    "tops": "tops-shirts",
    "shirts": "tops-shirts",
    "shoes": "footwear",
    "jeans": "denim",
}


def _svg(name, size, extra_class=""):
    body = _PATHS.get(name) or _PATHS.get(_ALIASES.get(name, ""), _PATHS["tag"])
    cls = ("ico " + extra_class).strip()
    return mark_safe(
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


@register.simple_tag
def icon(name, size=24, extra_class=""):
    """Render a UI icon by name, e.g. {% icon 'search' 20 %}."""
    return _svg(name, size, extra_class)


@register.simple_tag
def cat_icon(slug, size=24, extra_class=""):
    """Render a category icon by its slug."""
    return _svg(slug, size, extra_class)
