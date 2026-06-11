# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('upload/<str:file_type>/', views.upload_file, name='upload_file'),
    path('files/<str:file_type>/', views.file_list, name='file_list'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('share/<int:file_id>/', views.share_file, name='share_file'),
]