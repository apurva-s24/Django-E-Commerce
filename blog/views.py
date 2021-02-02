
from django.shortcuts import render
from django.http import HttpResponse
from . models import Blogpost

# Create your views here.


def index(request):
    myposts = Blogpost.objects.all()
    print(myposts)
    return render(request, 'blog/index.html', {'myposts': myposts})


def blogpost(request, id2):
    post = Blogpost.objects.filter(post_id=id2)[0]
    print(post)
    return render(request, 'blog/blogpost.html', {'post': post})
