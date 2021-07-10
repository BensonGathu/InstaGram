from . models import Image
from django import forms

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','image_name','image_caption']