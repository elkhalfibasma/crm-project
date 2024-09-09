from django.urls import path
from . import views
from leads import views as lead_views
from django.conf import settings
from django.conf.urls.static import static
from .views import import_google_ads_leads

urlpatterns = [
    # Routes pour les leads
    path('leads/list', views.lead_list, name='lead_list'),
    path('leads/add/', views.lead_add, name='lead_add'),
    path('leads/edit/<int:lead_id>/', views.lead_edit, name='lead_edit'),
    path('leads/delete/<int:lead_id>/', views.lead_delete, name='lead_delete'),
    path('leads/import/', views.lead_import, name='lead_import'),
    path('leads/assign/<int:lead_id>/', views.lead_assign, name='lead_assign'),
    path('leads/<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('leads/interactions/<int:lead_id>/', views.interaction_view, name='lead_interactions'),
    path('leads/historique_appels/<int:lead_id>/', views.historique_appels, name='historique_appels'),

    # Routes pour les actions
    path('leads/', lead_views.lead_actions, name='lead_actions'),
    path('BoiteGmail/<int:lead_id>', views.BoiteGmail, name='BoiteGmail'),
    # Autres pages
    path('faq/', views.faq, name='faq'),
    path('support-guide/', views.SupportGuideView.as_view(), name='support_guide'),
    path('import-google-ads/', import_google_ads_leads, name='import_google_ads_leads'),
    path('api/lead-statistics/', views.get_lead_statistics, name='lead_statistics'),
    path('lead_ac/', views.lead_ac, name='lead_ac'),
    path('send_email/<int:lead_id>/', views.send_email, name='send_email'),
    path('historique_emails/<int:lead_id>', views.historique_emails, name='historique_emails'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
