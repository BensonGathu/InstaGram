from django.shortcuts import render,redirect
from . models import Profile,Image,Comment,Follow
from . forms import UploadImageForm,CreateUserForm,UpdateProfileForm
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
            name = form.cleaned_data.get("username")
            messages.success(request,name+"'s account successfully created")
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
        else:
            messages.info(request, 'Incorrect Username or Password')
            
    context = {}
    return render(request,'registration/login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def index(request):
    all_images = Image.all_images()
    
    return render(request,"index.html",{"all_images":all_images})

@login_required(login_url="login")
def comments(request,id):
    image_id= request.GET.get("comments_image_id")

    all_comments = Comment.get_comments(id)
    comments = []
    return render(request,"comments.html",{"all_comments":all_comments})

@login_required(login_url="login")
def profile(request):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        prof_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {"images":images,"profile_form":profile_form})
    # user = request.user
    # profile = User.objects.filter(user = user)
    # # ppic = profile.profile_photo

    # images = Image.objects.filter(user =user).all()

    # return render("profile.html",{"images":images,"profile":profile})


@login_required(login_url="login")
def upload_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST or None,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user.profile
            image.save()
        return redirect('index')
    else:
        form = UploadImageForm()
    return render(request,'image.html',{"form":form})

@login_required(login_url="login")
def search_profile(request):
    if 'username' in request.GET and request.GET["username"]:
        search_name = request.GET.get("username")
        searched_profiles = Profile.search_profile(search_name)
        message = f"{search_name}"

        return render(request,"search.html",{"message":message,"searched_profiles":searched_profiles})
    else:
        message = "Enter a username to search"
        return render(request,"search.html",{"message":message})

@login_required(login_url='login')
def follow(request,pk):
    if request.method == "GET":
        user = Profile.objects.get(pk=pk)
        follow = Follow(following=request.user.profile,followers=user)
        follow.save()
        return redirect('profile')

def unfollow(request,pk):
    if request.method == 'GET':
        user = Profile.objects.get(pk=pk)
        unfollow = Follow.objects.filter(following=request.user.profile,followers=user)
        unfollow.delete()
        return redirect('profile')