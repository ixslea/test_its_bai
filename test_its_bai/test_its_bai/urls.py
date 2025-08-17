from django.urls import path, re_path
from live_love_laugh import views
 
urlpatterns = [
    path("", views.index, name="quote"),
    re_path(r"^add", views.add, name="add"),
    re_path(r"^list", views.list, name="list"),
    re_path(r"^how_to", views.how_to, name="how_to"),
    path("quote/<int:quote_id>/", views.quote_details, name="quote_details"),
    path('like/<int:quote_id>/', views.like_quote, name='like_quote'),
] 