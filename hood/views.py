from django.http import response
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Hood, Profile, Business, Post
from django.http import Http404
from .forms import *
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import HoodSerializer,ProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from hood import serializer

# Create your views here.
@login_required(login_url='accounts/login/')
def index(request):
    try:
        hoods = Hood.objects.all()
    except Exception as e:
        raise Http404
    return render(request, "main/index.html", {"hoods": hoods})

@login_required(login_url='accounts/login/')
def create_hood(request):
    if request.method == "POST":
        form = HoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit = False)
            hood.save()
        return redirect("home")
    else:
        form = HoodForm()
    return render(request, "main/create_hood.html", {"form": form})

@login_required(login_url='accounts/login/')
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm()
    return render(request, "main/profile.html", {"form": form, "profile": profile})

@login_required(login_url='accounts/login/')
def post(request):
    posts = Post.objects.all().order_by('-posted_on')
    return render(request, "main/post.html", {"posts": posts})

@login_required(login_url='accounts/login/')
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.hood = request.user.profile.neighborhood
            post.posted_by = request.user
            post.save()
            return redirect("post")
    else:
        form = PostForm()
    return render(request, "main/new_post.html", {"form": form})

@login_required(login_url='accounts/login/')
def new_biz(request):
    user = User.objects.filter(id = request.user.id).first()
    profile = Profile.objects.filter(user = user).first()
    if request.method == "POST":
        business_form = BusinessForm(request.POST, request.FILES)
        if business_form.is_valid():
            business = Business(name = request.POST['name'], neighborhood = profile.neighborhood)
            business.save()
        return redirect('business')
    else:
        business_form = BusinessForm()
    return render(request, "main/new_biz.html", {"business": business_form})


@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')

@login_required(login_url='/accounts/login/')
def apiView(request):
    data = {}
    current_user = request.user
    profiles = Profile.objects.filter(user = current_user)[0:1]
    

    return render(request, "api/api.html", {"profile": profiles})

class ProfileList(APIView):
    def get(self, request, format = None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many = True)

        return Response(serializers.data)

class HoodList(APIView):
    def get(self, request, format = None):
        all_hoods = Hood.objects.all()
        serializers = HoodSerializer(all_hoods, many = True)

        return Response(serializers.data)

@api_view(['POST'])
def token(request):
    current_user = request.user
    if request.method == "POST":
        serializer = ProfileSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            account = current_user
            token = Token.objects.get(user = account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

