# Create your views here.
from django.shortcuts import render , redirect
from django.http import HttpResponse
def index(request):
    return render(request, "index.html")

def services(request):
    return render(request, "services.html")
