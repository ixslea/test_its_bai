from django.urls import path, re_path
from live_love_laugh import views
 
urlpatterns = [
    path("", views.index, name="quote"),
    re_path(r"^add", views.add, name="add"),
    re_path(r"^list", views.list, name="list"),
] 