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
    