from django.forms import ModelForm, CheckboxSelectMultiple
from django.contrib.auth.models import Group
from shopapp.models import Product, Order
from django.forms import forms
from django import forms


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount'


class CreateNewOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_adress', 'promocode', 'user', 'products'
        widgets = {
            'products': CheckboxSelectMultiple(),
        }


# class UpdateOrderForm(ModelForm):
#
#     class Meta:
#         model = Order
#         fields = 'delivery_adress', 'promocode', 'user', 'products'
#         widgets = {
#             'products': CheckboxSelectMultiple(),
#         }


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', ]


class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = "name", "price", "discription", "discount", "preview"

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
