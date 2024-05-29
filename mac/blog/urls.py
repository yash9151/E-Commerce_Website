from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="BlogHome"),
    path('blogpost/', views.blogpost, name="blogPost"),
]
