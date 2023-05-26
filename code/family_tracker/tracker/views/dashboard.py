from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from tracker.models import User

@require_http_methods(['GET'])
def dashboard(request):
    try:
        user = User.objects.get(token=request.session['token'])
    except KeyError:
        return redirect("/login")
    else:
        userdata = {
            'user': user,
            'groups': user.groups,
            'calendar': user.calendar
        }
        return render(request, 'tracker/dashboard.html', userdata)