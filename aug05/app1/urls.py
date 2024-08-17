from django.urls import path
from app1 import views 


urlpatterns=[
    path('',views.home,name="homepage"),
    path('login',views.loginV,name="loginpage"),
    path('profile',views.profile,name="profilepage"),
    path('logout',views.logoutV,name="logoutpage"),
    path('register',views.register,name="registerpage"),
    path('create',views.tweetView,name='createpost'),
    path('delete/<int:rid>',views.deleteView,name='deletepost'),
    path('display/<int:rid>',views.display,name='showPost'),

]