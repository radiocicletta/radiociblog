from django.contrib.auth.models import User
from profiles.models import UserProfile
from blog.models import Post
from django.shortcuts import render


def show_profile(request, nickname):
    profile = None
    if nickname:
        profile = UserProfile.objects.filter(nickname=nickname)
        if profile:
            user = profile[0].user
            profile = profile[0]
            posts = Post.objects.filter(author=user).order_by('-published_on')
        else:
            user = User.objects.filter(username=nickname)
            if user:
                profile = user[0].profile
                posts = Post.objects.filter(author=user[0]).order_by('-published_on')
    return render(request, 'profiles/show.html', {'profile': profile, 'posts': posts})


def all_profiles(request):
    profiles = UserProfile.objects.all()
    return render(request, 'profiles/list.html', {'profiles': profiles})
