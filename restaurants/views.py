from typing import ContextManager
from django.shortcuts import render, redirect

from .models import Restaurant
from .forms import RestaurantForm

# Create your views here.
#def index(request, restaurant_id):
    #restaurants = Restaurant.order_by('restaurantName')

    #restaurants = Restaurant.objects.get(id=restaurant_id)
    #context = {'restaurants' : restaurants}
def index(request):
    #return render(request, 'restaurants/index.html', context)
    return render(request, 'restaurants/index.html')

def restaurants(request):
    restaurantsList = Restaurant.objects.order_by('restaurantName')
    context = {'restaurants' : restaurantsList}
 
    return render(request, 'restaurants/restaurants.html', context)

def restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    restaurantType = restaurant.restaurantType
    context = {'restaurant' : restaurant, 'restaurantType' : restaurantType}
    return render(request, 'restaurants/restaurant.html', context)

def new_restaurant(request):
    if request.method !=  'POST':
        form = RestaurantForm()

    else:
        form = RestaurantForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurants:restaurants')

    context = {'form': form}
    return render(request, 'restaurants/new_restaurant.html', context)

def faq(request):
    return render(request, 'restaurants/faq.html')

def about(request):
    return render(request, 'restaurants/about.html')
