from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect

def LogOut(request):
    logout(request)
    return redirect('login')