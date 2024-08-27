# leads/views.py
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Lead
from notifications.models import Notification  # Import Notification from the notifications app
from .forms import LeadForm
from .forms import AssignLeadForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import csv
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
import openpyxl
from django.db.models import Q
#new
from django.db.models.functions import TruncDate 
from django.db.models import Count
from django.utils.dateparse import parse_date
from notifications.models import Notification  # Import the Notification model
from django.http import JsonResponse
from .api_integration import fetch_google_ads_data
@login_required


def lead_list(request):
    # Get status choices from the Lead model
    statut_choices = Lead._meta.get_field('statut').choices
    
    # Get filters from the request
    statut_filter = request.GET.get('statut', 'all')
    created_at_filter = request.GET.get('crée', None)

    # Count leads for each status
    statut_counts = {
        'nouveau': Lead.objects.filter(statut='nouveau').count(),
        'Contacté': Lead.objects.filter(statut='Contacté').count(),
        'Perdu': Lead.objects.filter(statut='Perdu').count(),
    }
    
    # Query leads and apply filters
    leads = Lead.objects.all()

    # Apply status filter
    if statut_filter != 'all':
        leads = leads.filter(statut=statut_filter)

    # Apply date filter
    if created_at_filter:
        try:
            parsed_date = parse_date(created_at_filter)
            if parsed_date:
                leads = leads.annotate(date=TruncDate('crée')).filter(date=parsed_date)
        except ValueError:
            print('Invalid date format')

    # Query leads that are pending follow-up (not assigned)
    leads_pending_followup = Lead.objects.filter(Assigné__isnull=True)
   
    # Filtrer les leads pris en charge
    leads_pris_en_charge = Lead.objects.filter(Assigné__isnull=False)
    
    # Filtrer les leads non pris en charge
    leads_non_pris_en_charge = Lead.objects.filter(Assigné__isnull=True)
    
    # Filtrer les leads pris en charge et dont le statut est différent de 'Contacté'
    leads_non_contactes = Lead.objects.filter(~Q(statut='Contacté'))
    
    # Compter le nombre de leads pris en charge
    nombre_leads_pris_en_charge = leads_pris_en_charge.count()
    
    # Compter le nombre de leads non pris en charge
    nombre_leads_non_pris_en_charge = leads_non_pris_en_charge.count()
    
    # Compter le nombre de leads pris en charge et non contactés
    nombre_leads_non_contactes = leads_non_contactes.count()

    # Trier les leads par date de création décroissante et limiter à 4
    leads = leads.order_by('-crée')[:4]

    # Indiquer si le bouton "Voir plus" doit être affiché
    show_voir_plus = leads.count() == 4

    context = {
        'nombre_leads_pris_en_charge': nombre_leads_pris_en_charge,
        'nombre_leads_non_pris_en_charge': nombre_leads_non_pris_en_charge,
        'nombre_leads_non_contactes': nombre_leads_non_contactes,
        'leads': leads,
        'statut_choices': statut_choices,
        'created_at_filter': created_at_filter,
        'statut_counts': statut_counts,
        'leads_pending_followup': leads_pending_followup,
        'show_voir_plus': show_voir_plus,  # Pour savoir si afficher le bouton "Voir plus"
    }
    return render(request, 'lead_list.html', context)


   
def faq(request):
    return render(request, 'faq.html')
from django.views.generic import TemplateView

class SupportGuideView(TemplateView):
    template_name = 'support_guide.html'

def lead_detail(request, lead_id):
    lead = Lead.objects.get(id=lead_id)
    return render(request, 'lead_detail.html', {'lead': lead})
from .models import Lead, Interaction
from django.shortcuts import render, redirect
from .models import Lead, Interaction
from .forms import InteractionForm


from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead, Interaction
from .forms import AppelForm
import openpyxl
import os

def interaction_view(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST" and 'appel_form' in request.POST:
        form = AppelForm(request.POST)
        if form.is_valid():
            # Sauvegarde de l'appel dans la base de données
            appel = form.save(commit=False)
            appel.lead = lead
            appel.save()

            # Sauvegarde des informations dans un fichier Excel
            file_path = save_call_to_excel(lead)

            return redirect('lead_interactions', lead_id=lead.id)
    else:
        form = AppelForm()

    interactions_telephonique = Interaction.objects.filter(lead=lead, type="Appel")
    interactions_email = Interaction.objects.filter(lead=lead, type="Email")
    
    # Chemin d'accès au fichier Excel
    file_path = f"media/{lead.id}_interactions_appels.xlsx"

    return render(request, 'lead_interactions.html', {
        'lead': lead,
        'appel_form': form,
        'interactions_telephonique': interactions_telephonique,
        'interactions_email': interactions_email,
        'excel_file_path': file_path,
    })

def save_call_to_excel(lead):
    file_path = f"media/{lead.id}_interactions_appels.xlsx"

    try:
        # Ouvrir le fichier Excel existant
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    except FileNotFoundError:
        # Créer un nouveau fichier Excel s'il n'existe pas
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # Créer l'en-tête
        sheet.append(["Lead ID", "Nom", "Prénom", "Date", "Type", "Détails", "Durée", "Commentaires"])

    # Ajouter les détails de l'appel dans une nouvelle ligne
    sheet.append([
        lead.id,
        lead.Nom,
        lead.Prénom,
        lead.date,
        "Appel",
        lead.details,
        lead.duree,
        lead.commentaires,
    ])

    # Sauvegarder le fichier Excel
    workbook.save(file_path)

    return file_path


#modification pour les notifications
@login_required
def lead_add(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.save()

            # Crée une notification pour le nouveau lead
            Notification.objects.create(
                user=request.user,  # Supposons que la notification est pour l'utilisateur qui a ajouté le lead
                message=f'Un nouveau lead "{lead.Prénom}" a été ajouté.',
                type='lead'
            )
            return redirect('lead_actions')
        else:
            print(form.errors)  # Affiche les erreurs du formulaire pour le débogage
    else:
        form = LeadForm()

    return render(request, 'lead_form.html', {'form': form})
def lead_delete(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        lead.delete()
        return redirect('lead_list')  # Redirection vers la liste des leads après suppression réussie
    return render(request, 'lead_confirm_delete.html', {'lead': lead})
def lead_edit(request, lead_id):
    # Récupérer le lead basé sur l'ID
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            # Redirection vers la liste des leads après modification réussie
            return redirect('lead_actions')  # Vous pouvez changer 'lead_actions' si nécessaire
    else:
        form = LeadForm(instance=lead)

    return render(request, 'lead_form.html', {'form': form, 'lead': lead})
def lead_import(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
        except UnicodeDecodeError:
            decoded_file = csv_file.read().decode('latin-1').splitlines()
        
        reader = csv.DictReader(decoded_file)
        
        for row in reader:
            Lead.objects.create(
    Prénom=row['Prénom'],
    Nom=row['Nom'],
    Email=row['Email'],
    Télephone=row['Télephone'],
    source=row['source'],
    statut=row['statut'],
    notes=row.get('notes', ''),
)

        messages.success(request, 'Leads importés avec succès.')
        return redirect('lead_list')

    return render(request, 'lead_import.html')

def lead_api_import(request):
    # Code for API integration to import leads automatically
    return HttpResponse("API Integration for lead import")


@login_required
def lead_assign(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if not lead.Assigné and request.user.is_authenticated:
        lead.Assigné = request.user
        lead.save()
    return redirect('lead_list')


def lead_actions(request):
    # Fetch leads or perform any necessary logic here
    leads = Lead.objects.all()  # Adjust the query as needed
    
    return render(request, 'lead_actions.html', {'leads': leads})


# Access all leads assigned to a specific user
#assigned_leads = user.assigned_leads.all()
from django.shortcuts import render
# Vue basée sur une classe
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


from django.shortcuts import render
from .models import Lead

def dashboard(request):
    # Filtrer les leads non pris en charge et les ordonner par date de création
    leads_pending_followup = Lead.objects.filter(assigné__isnull=True).order_by('crée')[:3]
    context = {
        'leads_pending_followup': leads_pending_followup,
    }
    return render(request, 'dashboard.html', context)

def import_google_ads_leads(request):
    access_token = 'YOUR_GOOGLE_ACCESS_TOKEN'
    data = fetch_google_ads_data(access_token)

    # Exemple d'importation des données
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

    return JsonResponse({'status': 'success', 'data': data})

from django.http import JsonResponse
from .models import Lead

def get_lead_statistics(request):
    tasks_accomplished = Lead.objects.filter(contacted=True).count()
    tasks_not_accomplished = Lead.objects.filter(contacted=False).count()
    
    # Ajoutez des statistiques supplémentaires si nécessaire
    data = {
        'tasks_accomplished': tasks_accomplished,
        'tasks_not_accomplished': tasks_not_accomplished,
        'meetings_upcoming': 5,  # Exemple statique, remplacez par des données réelles
        'emails_pending': 8  # Exemple statique, remplacez par des données réelles
    }
    
    return JsonResponse(data)
