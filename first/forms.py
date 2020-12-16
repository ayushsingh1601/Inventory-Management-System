from django import forms
from .models import *
class inventoryForm(forms.ModelForm):
    class Meta:
        model = inventory
        fields = ('brand', 'model_name', 'model_number', 'price', 'starting_inventory', 'supplier_id', 'minimum_required',)
class suppliersForm(forms.ModelForm):
    class Meta:
        model = suppliers
        fields = ('supplier_name',)
class ordersForm(forms.ModelForm):
    class Meta:
        model = orders
        fields = ('first_name', 'last_name', 'product_id', 'number_shipped',)
class purchasesForm(forms.ModelForm):
    class Meta:
        model = purchases
        fields = ('product_id', 'number_received',)
class to_orderForm(forms.ModelForm):
    class Meta:
        model = to_order
        fields = ('supplier_id', 'model_number', 'number',)
