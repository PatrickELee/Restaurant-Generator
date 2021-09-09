from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'restaurants/index.html')

def faq(request):
    return render(request, 'restaurants/faq.html')

def about(request):
    return render(request, 'restaurants/about.html')
