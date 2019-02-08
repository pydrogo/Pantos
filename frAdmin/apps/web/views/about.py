from django.shortcuts import render, get_object_or_404, redirect



def About(request):
    return render(request, 'about.html')
