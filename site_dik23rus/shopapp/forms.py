from django.forms import ModelForm, CheckboxSelectMultiple
from django.contrib.auth.models import Group
from shopapp.models import Product, Order


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
        fields = ['name',]