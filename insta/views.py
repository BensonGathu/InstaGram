from django.shortcuts import render,redirect,get_object_or_404
from . models import Profile,Image,Comment,Follow
from . forms import UploadImageForm,CreateUserForm,UpdateProfileForm,NewCommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


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
    all_comments = Comment.get_comments(id)
    image = get_object_or_404(Image, pk=id)
    
    form = NewCommentForm()
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.author = request.user
            comment.save()
        return HttpResponseRedirect(request.path_info)       
        # return redirect('comments')

    else:
        form = NewCommentForm()
    return render(request,"comments.html",{"all_comments":all_comments,"form":form})

@login_required(login_url="login")
def profile(request):
    images = request.user.profile.images.all()
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
        return redirect('publicprofile',user.user.username)

def unfollow(request,pk):
    if request.method == 'GET':
        user = Profile.objects.get(pk=pk)
        unfollow = Follow.objects.filter(following=request.user.profile,followers=user)
        unfollow.delete()
        return redirect('publicprofile',user.user.username)

@login_required(login_url='login')
def publicprofile(request, username):
    user_profile = get_object_or_404(User, username=username)
    if request.user == user_profile:
        return redirect('profile')
    user_posts = user_profile.profile.images.all()
    followers = Follow.objects.filter(followers=user_profile.profile)
    status = None
    for follower in followers:
        if request.user.profile == follower.following:

            status = True
    
        else:
            status = False
    return render(request, 'public_profile.html', {"user_profile":user_profile,"user_posts":user_posts,"followers":followers,"status":status})

