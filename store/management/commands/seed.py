from decimal import Decimal

from django.core.management.base import BaseCommand

from store.models import Category, Product

IMG = "https://images.unsplash.com/photo-{}?w=800&q=80&auto=format&fit=crop"

CATEGORIES = [
    ("Dresses", "👗", "Effortless day-to-night silhouettes", 1, "1485462537746-965f33f7f6a7"),
    ("Tops & Shirts", "👕", "Everyday staples with a twist", 2, "1620799140408-edc6dcb6d633"),
    ("Denim", "👖", "Selvedge, raw and washed blues", 3, "1541099649105-f69ad21f3246"),
    ("Outerwear", "🧥", "Coats and jackets for every season", 4, "1543076447-215ad9ba6923"),
    ("Footwear", "👟", "Sneakers, heels and boots", 5, "1595950653106-6c9ebd614d3a"),
    ("Bags", "👜", "Totes, crossbodies and clutches", 6, "1584917865442-de89df76afd3"),
    ("Accessories", "🕶", "The finishing touches", 7, "1511499767150-a48a237f0083"),
    ("Activewear", "🏃", "Move-with-you performance fits", 8, "1517836357463-d25dfeac3438"),
]

# (category, name, price, color, sizes, featured, image_id, description)
PRODUCTS = [
    ("Dresses", "Amara Slip Dress", "89.00", "Champagne", "XS,S,M,L", True,
     "1595777457583-95e059d581b8", "A bias-cut satin slip that skims the body and catches the light."),
    ("Dresses", "Lumen Linen Midi", "74.00", "Sand", "S,M,L,XL", True,
     "1539109136881-3be0616acf4b", "Breathable linen with a relaxed midi length for warm days."),
    ("Dresses", "Noir Wrap Dress", "96.00", "Black", "XS,S,M,L", False,
     "1485462537746-965f33f7f6a7", "A timeless wrap silhouette that flatters every frame."),
    ("Dresses", "Rosa Floral Sundress", "68.00", "Blush Floral", "S,M,L", False,
     "1596609548086-85bbf8ddb6b9", "Light, floaty and printed with hand-drawn florals."),
    ("Dresses", "Ivy Evening Gown", "148.00", "Emerald", "XS,S,M,L", True,
     "1490481651871-ab68de25d43d", "Floor-sweeping gown for the moments that matter."),

    ("Tops & Shirts", "Studio Cotton Tee", "28.00", "White", "XS,S,M,L,XL", True,
     "1521572163474-6864f9cf17ab", "Heavyweight organic cotton with a clean boxy cut."),
    ("Tops & Shirts", "Atelier Oxford Shirt", "58.00", "White", "S,M,L,XL", False,
     "1620799140408-edc6dcb6d633", "A crisp oxford shirt tailored for a modern fit."),
    ("Tops & Shirts", "Marlow Knit Polo", "52.00", "Sage", "S,M,L,XL", False,
     "1602810318383-e386cc2a3ccf", "Fine-gauge knit polo that dresses up or down."),
    ("Tops & Shirts", "Heron Linen Shirt", "64.00", "Stone", "S,M,L,XL", True,
     "1552374196-c4e7ffc6e126", "Airy linen with a lived-in, laid-back drape."),

    ("Denim", "1954 Straight Jean", "92.00", "Mid Blue", "26,28,30,32,34", True,
     "1541099649105-f69ad21f3246", "Rigid selvedge denim with a classic straight leg."),
    ("Denim", "Haze Mom Jean", "84.00", "Light Wash", "24,26,28,30,32", False,
     "1542272604-787c3835535d", "High-rise mom fit with a vintage-inspired wash."),
    ("Denim", "Onyx Skinny Jean", "78.00", "Black", "26,28,30,32", False,
     "1475178626620-a4d074967452", "A sleek skinny that holds its shape all day."),

    ("Outerwear", "Camden Trench Coat", "168.00", "Camel", "S,M,L,XL", True,
     "1434389677669-e08b4cac3105", "A double-breasted trench cut from water-repellent cotton."),
    ("Outerwear", "Alpine Puffer Jacket", "134.00", "Slate", "S,M,L,XL", True,
     "1591047139829-d91aecb6caea", "Lightweight down-alternative warmth without the bulk."),
    ("Outerwear", "Rue Denim Jacket", "88.00", "Indigo", "S,M,L,XL", False,
     "1551232864-3f0890e580d9", "The everyday trucker jacket in rigid indigo denim."),
    ("Outerwear", "Kestrel Wool Coat", "196.00", "Charcoal", "S,M,L,XL", False,
     "1543076447-215ad9ba6923", "A tailored wool-blend overcoat with a clean lapel."),

    ("Footwear", "Cloud Runner Sneaker", "112.00", "Off White", "6,7,8,9,10,11", True,
     "1560769629-975ec94e6a86", "Cushioned everyday trainer with a breathable knit upper."),
    ("Footwear", "Court Classic Low", "98.00", "White/Green", "6,7,8,9,10,11", False,
     "1595950653106-6c9ebd614d3a", "A retro court sneaker that pairs with everything."),
    ("Footwear", "Scarlet Heel", "124.00", "Red", "5,6,7,8,9", True,
     "1542291026-7eec264c27ff", "A confident block heel in smooth scarlet leather."),
    ("Footwear", "Metro Runner", "108.00", "Grey", "6,7,8,9,10,11,12", False,
     "1549298916-b41d501d3772", "Streamlined runner built for city miles."),
    ("Footwear", "Aria Strap Heel", "118.00", "Nude", "5,6,7,8,9", False,
     "1441984904996-e0b6ba687e04", "Delicate ankle-strap heel for evenings out."),

    ("Bags", "Metropolitan Tote", "138.00", "Tan", "One Size", True,
     "1584917865442-de89df76afd3", "A structured leather tote roomy enough for the day."),
    ("Bags", "Lyric Crossbody", "96.00", "Black", "One Size", True,
     "1548036328-c9fa89d128fa", "Compact crossbody with an adjustable webbing strap."),
    ("Bags", "Field Backpack", "108.00", "Olive", "One Size", False,
     "1553062407-98eeb64c6a62", "Water-resistant everyday pack with a padded sleeve."),
    ("Bags", "Petal Shoulder Bag", "84.00", "Cream", "One Size", False,
     "1596755094514-f87e34085b2c", "A soft slouchy shoulder bag in buttery faux leather."),

    ("Accessories", "Halo Sunglasses", "42.00", "Tortoise", "One Size", True,
     "1511499767150-a48a237f0083", "UV400 acetate frames with a timeless silhouette."),
    ("Accessories", "Retro Round Shades", "38.00", "Gold", "One Size", False,
     "1572635196237-14b3f281503f", "Slim metal rounds for a vintage finish."),
    ("Accessories", "Meridian Watch", "156.00", "Silver", "One Size", True,
     "1523275335684-37898b6baf30", "A minimalist automatic watch with a steel mesh band."),
    ("Accessories", "Nova Leather Watch", "128.00", "Brown", "One Size", False,
     "1524805444758-089113d48a6d", "Warm leather strap paired with a clean cream dial."),

    ("Activewear", "Flux Training Tee", "34.00", "Black", "XS,S,M,L,XL", True,
     "1517836357463-d25dfeac3438", "Sweat-wicking, four-way stretch tee for the gym."),
    ("Activewear", "Momentum Leggings", "56.00", "Charcoal", "XS,S,M,L,XL", True,
     "1594381898411-846e7d193883", "High-rise compression leggings with a hidden pocket."),
    ("Activewear", "Pace Running Set", "72.00", "Navy", "S,M,L,XL", False,
     "1506629082955-511b1aa562c8", "A breathable short-and-top set built to move."),
]


class Command(BaseCommand):
    help = "Seed DK Fashions with categories and a starter catalogue."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh", action="store_true",
            help="Delete existing categories/products before seeding.",
        )

    def handle(self, *args, **opts):
        if opts["fresh"]:
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing catalogue."))

        cats = {}
        for name, emoji, tagline, order, img in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"emoji": emoji, "tagline": tagline, "order": order},
            )
            cat.emoji = emoji
            cat.tagline = tagline
            cat.order = order
            cat.image_url = IMG.format(img)
            cat.save()
            cats[name] = cat
        self.stdout.write(self.style.SUCCESS(f"Categories: {len(cats)}"))

        created = 0
        for cat_name, name, price, color, sizes, featured, img_id, desc in PRODUCTS:
            product, was_created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": cats[cat_name],
                    "price": Decimal(price),
                    "color": color,
                    "sizes": sizes,
                    "is_featured": featured,
                    "image_url": IMG.format(img_id),
                    "description": desc,
                    "in_stock": True,
                },
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(
            f"Products created: {created} (total {Product.objects.count()})"
        ))
        self.stdout.write(self.style.SUCCESS("Done. Fire up the server and shop."))
