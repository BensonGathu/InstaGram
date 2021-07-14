from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name="index"),
    path('comment/<int:id>',views.comments,name="comments"),
    path('new/image/', views.upload_image, name='new-image'),
    path('register/',views.register,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('search/',views.search_profile,name='search_results'),
    path('comments/',views.comments,name='comments'),
    path('follow/<pk>',views.follow,name='follow'),
    path('unfollow/<pk>',views.unfollow,name='unfollow'),
    path('publicprofile/<username>',views.publicprofile,name="publicprofile"),
    path('newprofile/',views.myprofile,name="newprofile"),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
