from django.contrib.auth.models import User
from blog.models import Post
from django.shortcuts import get_object_or_404, render

def show_profile(request, nickname):
    profile = None
    if nickname:
        user = User.objects.filter(username = nickname)
        if user :
            profile = user[0].profile
            posts = Post.objects.filter(author = user[0]).order_by('-published_on')
    return render(request, 'profiles/show.html', {'profile': profile, 'posts': posts})

def all_profiles(request):
    profiles = UserProfile.object.all()
    return render(request, 'profiles/list.html', {'profiles': profiles})
