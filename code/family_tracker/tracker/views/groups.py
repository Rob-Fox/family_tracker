from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from tracker.models import User

@require_http_methods(['GET', 'POST'])
def groups(request):
    if isinstance(request.session['user'], User):
        return render(request, 'login.html')

@require_http_methods(['POST', 'GET'])
def specific_group(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return HttpResponseRedirect('/login', errors)
    else:
        request.session['user'] = User.objects.get(username=request.POST['username'])
        return redirect('/')
    