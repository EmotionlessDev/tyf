from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/blank.html')

def profile(request):
    return render(request, 'main/profile.html')