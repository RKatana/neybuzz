from django import forms
from .models import Profile, Business, Hood, Post

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'image', 'neighborhood']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['user', 'name', 'description', 'neighborhood']

class HoodForm(forms.ModelForm):
    class Meta:
        model = Hood
        fields = ['user', 'name', 'description', 'location', 'population', 'image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'neighborhood', 'image']
