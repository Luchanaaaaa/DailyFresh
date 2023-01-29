from django.shortcuts import render

# Create your views here.

#http:// 127.0.0

def index(request):
    return render(request, 'index.html')
