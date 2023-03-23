from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutpage,name="logout"),
    path('signup/',views.signup,name="signup"),
    path('schedule/<str:user>/<str:projectname>',views.create_schedule,name="schedule"),
    path('main/<str:user>/<str:projectname>',views.main,name="main"),
    path('delete/<str:user>/<str:projectname>/<str:pk>',views.markasdone,name="markasdone"),
]