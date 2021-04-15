from rest_framework import serializers
from .models import Profile, Hood

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'image', 'neighborhood')

class HoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hood
        fields = ('name', 'description', 'location', 'population', 'image')