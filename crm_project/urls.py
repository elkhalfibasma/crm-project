from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from leads import views as lead_views
from appointments import views as appointments_views
from django.views.generic.base import RedirectView
from notifications import views as notifications_views  # Import the notifications view
from appointments import views as appointment_views
from django.conf import settings

from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),  # Utilisation de admin.site.urls pour l'administration Django
    path('', user_views.login_view, name='login'),  # Rediriger l'URL racine vers la page de connexion
    path('logout/', user_views.custom_logout, name='logout'),  # URL pour la déconnexion
    path('leads/', lead_views.lead_list, name='lead_list'),  # URL pour la liste des leads
    path('appointments/',appointments_views.appointments_list, name='appointments_list'), # URL pour la liste
    # Inclure les URL de l'application leads
    path('leads/', include('leads.urls')),
    path('appointments/', include('appointments.urls')),
    path('acceuil/', RedirectView.as_view(url='/', permanent=False)),
    path('notifications/', notifications_views.notifications_view, name='notifications'),  # URL for notifications
    path('conversations/', include('conversations.urls')),
    path('announcements_list/', user_views.announcements_list, name='announcements_list'), 
    path('announcements/new/', user_views.create_announcement, name='create_announcement'),
    path('', include('users.urls')),
    path('admin-dashboard/', user_views.admin_dashboard, name='admin_dashboard'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)