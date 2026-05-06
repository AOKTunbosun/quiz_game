from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing'),
    path('signup/', views.SignupPage.as_view(), name='signup'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('dashboard/', views.DashboardPage.as_view(), name='dashboard'),
    path('logout/', views.logout_user, name='logout')
]
