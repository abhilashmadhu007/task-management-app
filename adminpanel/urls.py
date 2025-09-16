"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from adminpanel import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # SuperAdmin
    path("manage-users/", views.manage_users, name="manage_users"),
    path("manage-admins/", views.manage_admins, name="manage_admins"),
    path("manage-tasks/", views.manage_tasks, name="manage_tasks"),
    path("task-reports/", views.task_reports, name="task_reports"),
    #admin
    path('admin-users/', views.user_list, name='user_list'),
    path('admin-tasks/', views.task_list, name='task_list'),
    path('admin-tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('admin-tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('admin-tasks/<int:task_id>/report/', views.view_task_report, name='view_task_report'),
]