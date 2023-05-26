from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tracker import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', )
]