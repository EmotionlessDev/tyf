from django.shortcuts import render, get_object_or_404
from users.models import User

def index(request):
    return render(request, 'main/blank.html')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'main/profile.html', {"user": user})
