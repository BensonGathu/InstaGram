from django.shortcuts import render
from . models import Profile,Image,Comment,Follow
# Create your views here.
def index(request):
    all_images = Image.all_images()
    return render(request,"index.html",{"all_images":all_images})
