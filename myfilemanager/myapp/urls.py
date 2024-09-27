from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    #project master
    #user 
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
]