# users/urls.py
from django.urls import path
from .views import (login_view, custom_logout, admin_dashboard,
                    LeadActionsView, AppointmentsListView, announcements_list,
                    create_announcement, edit_announcement, delete_announcement)
from users import views


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    
    
    path('appointments/', AppointmentsListView.as_view(), name='appointments_list'),
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/new/', views.create_announcement, name='create_announcement'),
    path('edit-announcement/<int:id>/', views.edit_announcement, name='edit_announcement'),
    path('annonce/supprimer/<int:id>/', views.delete_announcement, name='delete_announcement'),
]

