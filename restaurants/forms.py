from django import forms

from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurantName', 'restaurantType']
        labels = {'restaurantName': 'Restaurant Name', 'restaurantType' : 'Restaurant Type'}