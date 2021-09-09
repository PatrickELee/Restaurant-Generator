from django.urls import path
from . import views

app_name = 'restaurants'
urlpatterns = [
    path('', views.index, name='index'),
    path('faq', views.faq, name='faq'),
    path('about', views.about, name='about')
]