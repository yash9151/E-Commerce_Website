from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, "shop/index.html")

def about(request):
    return HttpResponse("We are in about page of shop")

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