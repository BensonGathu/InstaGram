from django.shortcuts import render
from . models import Profile,Image,Comment,Follow
from . forms import UploadImageForm,CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 


# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request,'registration/registration.html',context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
    context = {}
    return render(request,'registration/login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')


def index(request):
    all_images = Image.all_images()
    return render(request,"index.html",{"all_images":all_images})

def comments(request,id):
    all_comments = Comment.get_comments(id)
    return render(request,"index.html",{"all_comments":all_comments})

def Profile(request):
    profile = Profile.objects.filter(user = uname).first()
    images = Image.objects.filter(user =current_user.id).all()

    return render_template("profile.html",{"images":images,"profile":profile})

def upload_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('index')
    else:
        form = UploadImageForm()
    return render(request,'image.html',{"form":form})
    