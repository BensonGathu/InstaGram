from django.shortcuts import render
from . models import Profile,Image,Comment,Follow
from . forms import UploadImageForm
# Create your views here.
def index(request):
    all_images = Image.all_images()
    return render(request,"index.html",{"all_images":all_images})

def comments(request,id):
    all_comments = Comment.get_comments(id)
    return render(request,"index.html",{"all_comments":all_comments})

def Profile(request):
    profile = Profile.objects.filter(user = uname).first()
    images = Image.objects.filter(user =current_user.id).all()

    return render_template("profile.html", user = user,{"images":images,"profile":profile})

def upload_image(request):
    