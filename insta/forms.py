from . models import Image

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','image_name','image_caption']