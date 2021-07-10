from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    profile_photo = models.ImageField(upload_to = 'images',default='SOME IMAGE')
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls,name):
        return cls.objects.filter(user__username__icontains=name).all()


class Image(models.Model):
    image = models.ImageField(upload_to = 'images/',default='SOME IMAGE')
    image_name = models.CharField(max_length=50)
    image_caption = models.CharField(max_length=200)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile)
    date_created = models.DateTimeField(auto_now_add = True)


    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def update_caption(cls,new_caption):
        cls.objects.filter(id = 2 ).update(image_caption =new_caption)

    def all_likes(self):
        return self.likes.count()

    def __str__(self):
        return image_name



class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def save_comment(self):
        self.save()
        
    def __str__(self):
        return self.image
    def delete_comment(self):
        self.delete()
    
    @classmethod
    def get_comments(cls,image_id):
        return cls.objects.filter(image__id=image_id).all()


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='follower')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='followed')

    def __str__(self):
        return f'{self.follower} Follow'







