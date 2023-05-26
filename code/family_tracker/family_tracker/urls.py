"""
URL configuration for family_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from tracker import views

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include('tracker.urls')),
    # path('login/', views.login_page, name='login_page'),
    # path('login_attempt/', views.login_attempt, name='login_attempt'),
    # path('register/', views.register, name='register'),
    # path('registration_page/', views.registration_page, name='registration'),
    # path('', views.dashboard, name='dashboard'),
    # path('groups/', views.groups, name='groups'),
    # path('groups/<groupID>', views.specific_group, name='specific_group')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
