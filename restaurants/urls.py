from django.urls import path
from . import views

app_name = 'restaurants'
urlpatterns = [
    #Home Page
    #path('/<int:restaurant_id>/', views.index, name='index'),
    path('', views.index, name='index'),

    #Restaurants Page
    path('restaurants/',views.restaurants, name='restaurants'),
    
    path('restaurants/<int:restaurant_id>/', views.restaurant, name='restaurant'),
    
    path('new_restaurant/', views.new_restaurant, name='new_restaurant'),
    #FAQ Page
    path('faq/', views.faq, name='faq'),
    #About Page
    path('about/', views.about, name='about')
]