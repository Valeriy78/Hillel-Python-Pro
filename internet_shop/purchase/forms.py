"""
Purchase application forms
"""

from django import forms
from django.core.exceptions import ValidationError

from my_shop.models import Product
from purchase.models import OrderReturn


class CartItemForm(forms.Form):
    """Form for a new cart item"""

    product_id = forms.IntegerField(min_value=0, disabled=True, required=False)
    quantity = forms.IntegerField(min_value=0)

    def clean(self):
        super().clean()
        product_id = self.cleaned_data["product_id"]
        product = Product.objects.get(id=product_id)
        quantity = self.cleaned_data["quantity"]
        if quantity > product.quantity:
            raise ValidationError(f"There are only {product.quantity} units of this product in the shop")


class ConfirmForm(forms.Form):
    """Form for admin to confirm or reject"""

    decision = forms.ChoiceField(choices=OrderReturn.CHOICES, widget=forms.RadioSelect)
