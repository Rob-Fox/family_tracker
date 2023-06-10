from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
import bcrypt

from tracker.models import User
from tracker.serializers import *

@require_http_methods(['GET', 'POST'])
def login_page(request):
    return render(request, 'tracker/login.html')

@require_http_methods(['POST'])
def login_attempt(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return HttpResponseRedirect('/login', errors)
    else:
        request.session['token'] = User.objects.get(username=request.POST['username']).token
        return redirect('/')
    
@require_http_methods(['POST'])    
def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        # return HttpResponseRedirect('/registration_page', request.POST)
        print('request.post: {}'.format(request.POST))
        return render(request, 'tracker/register.html', request.POST)
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            name=request.POST['name'],
            username=request.POST['username'],
            password=password,
            token = bcrypt.hashpw(user.username.encode(), bcrypt.gensalt())
            )
        user.save()
        request.session['token'] = user.token
        return redirect('/')


@require_http_methods(['GET', 'POST'])
def registration_page(request):
    context = {
        'name': '',
        'email': '',
        'username': ''
    }
    return render(request, 'tracker/register.html', context)


class UserListCreateView(generics.ListCreateAPIView):
    """
        create:
            add users
        get:
            Search or get users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('email', 'username')

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        get:
            get a specific users details
        delete:
            remove an existing user
        patch:
            update one or more fields for an existing user
        put:
            update a user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer