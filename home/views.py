from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # return HttpResponse("Hello World!")
    return render(request,"Home/index.html")


def contact(request):
     return render(request,"Home/contact.html")

def About(request):
     return render(request,"Home/About.html")
