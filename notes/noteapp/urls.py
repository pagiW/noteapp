from django.urls import path
from .views import *

appurls = [
    path('', index),
    path('home/<str:id>', home),
    path('signup', signup),
    path('createnote/<str:id>', newnote),
    path('login', login),
    path('home/<str:id>/borrar/<int:note>', delete),
    path('home/<str:id>/mod/<int:note>', mod),
    path('home/<str:id>/borrar/<int:note>/conf', conf)
]