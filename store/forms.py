from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "email", "phone", "address", "city"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone (optional)"}),
            "address": forms.TextInput(attrs={"placeholder": "Street address"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
        }
