from django.urls import path
from . import views  # This imports views from the leads application
from leads import views as lead_views
from django.conf import settings
from django.conf.urls.static import static
from .views import import_google_ads_leads
urlpatterns = [
    path('leads/list', views.lead_list, name='lead_list'),
    path('<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('add/', views.lead_add, name='lead_add'),
    path('edit/<int:lead_id>/', views.lead_edit, name='lead_edit'),
    path('delete/<int:lead_id>/', views.lead_delete, name='lead_delete'),
    path('import/', views.lead_import, name='lead_import'),
    path('api/import/', views.lead_api_import, name='lead_api_import'),
    path('assign/<int:lead_id>/', views.lead_assign, name='lead_assign'),
    path('leads/', lead_views.lead_actions, name='lead_actions'),
    path('faq/', views.faq, name='faq'),
    path('import-google-ads/', import_google_ads_leads, name='import_google_ads_leads'),
    path('lead/<int:lead_id>/interactions/', views.interaction_view, name='lead_interactions'),
    path('support-guide/', views.SupportGuideView.as_view(), name='support_guide'),
    path('api/lead-statistics/', views.get_lead_statistics, name='lead_statistics'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

