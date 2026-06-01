from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('personal/', views.personal, name='personal'),
    path('new-application/', views.new_application, name='new_application'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
]