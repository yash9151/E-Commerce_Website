from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil

# Create your views here.
def index(request):
    # fetches products from database
    products = Product.objects.all()
    print(products)
    n=len(products)
    nSlides = n//4 + ceil((n/4) - (n//4))
    # params = {'product' : products, 'no_of_slides':nSlides, 'range' : range(1, nSlides)}

    allProds = [[products, range(1, nSlides), nSlides],
                [products, range(1, nSlides), nSlides]]
    params = {'allProds' : allProds}
    return render(request, "shop/index.html", params)

def about(request):
    return render(request, "shop/about.html")

def contact(request):
    return HttpResponse("We are in contact page of shop")

def tracker(request):
    return HttpResponse("We are in tracker page of shop")

def search(request):
    return HttpResponse("We are in search page of shop")

def prodView(request):
    return HttpResponse("We are in productview page of shop")

def checkout(request):
    return HttpResponse("We are in checkout page of shop")