from . models import Image,Profile,Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','image_name','image_caption']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']