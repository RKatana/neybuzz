from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name = 'home'),
    path("add_hood/", views.create_hood, name = "add_hood"),
    path("new_post/", views.new_post, name = "new_post"),
    path("posts/", views.post, name = "post"),
    path("profile/", views.profile, name = "profile"),
    path("business/", views.new_biz, name = "business"),
    path("logout/", views.logout, name = "logout"),
    path("api/hood/", views.HoodList.as_view()),
    path("api/profile/", views.ProfileList.as_view()),
    path("token/", obtain_auth_token, name = "token"),
    path("developer/api/", views.apiView, name = "api"),
]