from django.urls import path
from . import views

urlpatterns = [
    
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('edit/<int:appointment_id>/', views.appointment_edit, name='appointment_edit'),
    path('delete/<int:appointment_id>/', views.appointment_delete, name='appointment_delete'),
    path('<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),

]
