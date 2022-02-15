from typing import ContextManager
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from restaurants.api import FUSION_API, IPSTACK_API

from .models import Restaurant
from .forms import RestaurantForm

from dotenv import load_dotenv
from pathlib import Path

import random
import os

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

FUSION_API_KEY = os.getenv('FUSION_API_KEY')
IPSTACK_API_KEY = os.getenv('IPSTACK_API_KEY')


fusion_api = FUSION_API(FUSION_API_KEY)
ipstack_api = IPSTACK_API(IPSTACK_API_KEY)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    return render(request, 'restaurants/index.html')

@login_required
def restaurants(request):
    restaurantsList = Restaurant.objects.filter(owner=request.user).order_by('restaurantName')
    context = {'restaurants' : restaurantsList}
    return render(request, 'restaurants/restaurants.html', context)

@login_required
def restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if restaurant.owner != request.user:
        raise Http404
    ip = get_client_ip(request)
    ipstack_json = ipstack_api.get_ip_data(ip)
    long = ipstack_json['longitude']
    lat = ipstack_json['latitude']
    restaurant_data = fusion_api.search_buisness(restaurant.restaurantName, long, lat)
    restaurantType = restaurant.restaurantType
    context = {
        'restaurant' : restaurant,
        'restaurantType' : restaurantType,
        'restaurantID' : restaurant_id,
        'restaurant_data' : restaurant_data['businesses'][0]
    }
    return render(request, 'restaurants/restaurant.html', context)

@login_required
def random_restaurant(request):
    restaurantsList = Restaurant.objects.filter(owner=request.user)
    numRestaurants = len(restaurantsList)
    randomRestaurant = None
    randomRestaurantID = None
    if numRestaurants != 0:
        randomRestaurant = random.choice(restaurantsList)
        randomRestaurantID = randomRestaurant.id
    context = {'randomResult' : randomRestaurant, 'randomID' : randomRestaurantID}
    return render(request, 'restaurants/random_restaurant.html', context)

@login_required
def new_restaurant(request):
    if request.method !=  'POST':
        form = RestaurantForm()

    else:
        form = RestaurantForm(data=request.POST)
        if form.is_valid():
            new_restaurant = form.save(commit=False)
            new_restaurant.owner = request.user
            new_restaurant.save()
            return redirect('restaurants:restaurants')

    context = {'form': form}
    return render(request, 'restaurants/new_restaurant.html', context)

@login_required
def edit_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if restaurant.owner != request.user:
        raise Http404
    restaurantType = restaurant.restaurantType
    if request.method != 'POST':
        form = RestaurantForm(instance=restaurant)
    else:
        form = RestaurantForm(instance=restaurant, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurants:restaurant', restaurant_id = restaurant.id)
    context = {'restaurant' : restaurant, 'restaurantType' : restaurantType, 'form': form}
    return render(request, 'restaurants/edit_restaurant.html', context)
    
def faq(request):
    return render(request, 'restaurants/faq.html')

def about(request):
    return render(request, 'restaurants/about.html')
