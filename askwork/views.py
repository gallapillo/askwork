from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    hello = 'hello world'
    user = request.user
    context = {'user': user, 'hello': hello}
    return render(request, 'main/home.html', context)
