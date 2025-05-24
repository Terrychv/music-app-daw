from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def login_view(request):
    return render(request, 'users/login.html')

def signup_view(request):
    return render(request, 'users/signup.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')