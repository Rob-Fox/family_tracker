from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tracker import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_page, name='login_page'),
    path('dashboard/', views.dashboard, name='dashboard_page'),
    path('users/', views.UserListCreateView.as_view(), name='users_list'),
    path('user/<uuid:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]