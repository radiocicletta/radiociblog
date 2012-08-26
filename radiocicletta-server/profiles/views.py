from .models import UserProfile
from django.shortcuts import get_object_or_404, render

def show_profile(request, nickname):
    return render(request, 'profiles/show.html')

def all_profiles(request):
    return render(request, 'profiles/show.html')
