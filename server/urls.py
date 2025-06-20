from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('client_estimate/<int:pk>/', generate_client_estimate, name='client_estimate'),
    path('', show_total_projects, name='total_projects'),
    path('all_projects', show_list_projects, name='all_projects'),
    path('detail_project/<int:pk>/', show_detail_project, name='detail_project'),
    path('login', show_login, name='login'),
    path('register', show_register, name='register'),
    path('create_project', show_create_project, name='create_project'),
    path('main_customer/<int:pk>/', show_main_customer, name='main_customer'),
    path('project_estimates/<int:pk>/', show_project_estimates, name='project_estimates'),
    path('list_projects_customer', show_list_projects_customer, name='list_projects_customer'),

    path('list_task_adopted_admin/<int:pk>/', show_list_task_adopted_admin, name='list_task_adopted_admin'),
    path('detail_task_adopted_admin/<int:pk>/', show_detail_task_adopted_admin, name='detail_task_adopted_admin'),

    path('list_task_adopted_customer/<int:pk>/', show_list_task_adopted_customer, name='list_task_adopted_customer'),
    path('detail_task_adopted_customer/<int:pk>/', show_detail_task_adopted_customer, name='detail_task_adopted_customer')





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)