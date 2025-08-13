from django.urls import path, re_path
from live_love_laugh import views
 
urlpatterns = [
    path("", views.index, name="quote"),
    re_path(r"^add", views.add, name="add"),
    re_path(r"^list", views.list, name="list"),
    path("quote/<int:quote_id>/", views.quote_details, name="quote_details"),
    path('<int:quote_id>/like/', views.like_quote, name='like_quote'),
] 