from celery import shared_task
from .api_integration import fetch_google_ads_data
from .models import Lead

@shared_task
def import_google_ads_leads():
    access_token = 'YOUR_GOOGLE_ACCESS_TOKEN'
    data = fetch_google_ads_data(access_token)

    for item in data.get('results', []):
        Lead.objects.create(
            nom=item.get('ad_group_ad', {}).get('ad', {}).get('name', ''),
            prenom='',
            email='',
            telephone='',
            source='Google Ads',
            statut='Nouveau',
            note='',
            # Ajoute les autres champs nécessaires
        )

