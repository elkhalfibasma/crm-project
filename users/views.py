# users/views.py
from itertools import count
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from django.db.models import Count  # Importer Count depuis django.db.models

from appointments.models import Appointment
from leads.models import Lead

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirection en fonction du type d'utilisateur
            if user.is_staff or user.is_superuser:
                # Redirection pour les administrateurs
                return redirect('lead_list')  # Assurez-vous que 'admin_dashboard' est défini dans urls.py
            else:
                # Redirection pour les utilisateurs normaux
                return redirect('lead_list')  # Assurez-vous que 'lead_list' est défini dans urls.py
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.decorators import login_required
def custom_logout(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from appointments.models import Appointment
from leads.models import Lead
from django.db.models import Count


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from .models import Announcement
from .forms import AnnouncementForm
from .forms import CustomUserCreationForm
from django.contrib import messages

@login_required
def admin_dashboard(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Sauvegarde de l'utilisateur sans le commettre encore dans la base de données
            user = form.save(commit=False)
            
            # Hache le mot de passe correctement
            user.set_password(form.cleaned_data['password1'])
            
            # Assurez-vous que le compte est actif
            user.is_active = True
            
            # Sauvegarde de l'utilisateur dans la base de données
            user.save()
            
            # Affichage d'un message de succès
            messages.success(request, 'Utilisateur ajouté avec succès! L\'utilisateur peut maintenant se connecter.')
            
            # Rediriger vers le tableau de bord de l'administrateur pour afficher les messages
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Erreur lors de l\'ajout de l\'utilisateur.')
    else:
        form = CustomUserCreationForm()
    
    # S'assurer que le formulaire est toujours vide après une soumission réussie
    form = CustomUserCreationForm()
    
    # Récupérer et calculer les statistiques des leads et des rendez-vous
    leads = Lead.objects.all()
    leads_count = leads.count()
    converted_leads_count = leads.filter(statut='Converti').count()
    conversion_rate = (converted_leads_count / leads_count * 100) if leads_count > 0 else 0
    appointments = Appointment.objects.all()
    appointments_count = appointments.count()
    leads_pending_followup = leads.filter(Assigné__isnull=True).count()
    lead_sources = leads.values('source').annotate(count=Count('source')).order_by('source')
    sources = [source['source'] for source in lead_sources]
    counts = [source['count'] for source in lead_sources]
    new_leads_count = leads.filter(statut='Nouveau').count()
    lost_leads_count = leads.filter(statut='Perdu').count()
    
    # Récupérer les utilisateurs non administrateurs et non superutilisateurs
    utilisateurs = User.objects.filter(is_staff=False, is_superuser=False)
    leads_counts = [leads.filter(Assigné=user).count() for user in utilisateurs]
    recent_leads = leads.order_by('-crée')[:10]
    
    return render(request, 'admin_dashboard.html', {
        'form': form,
        'leads_count': leads_count,
        'appointments_count': appointments_count,
        'taux_conversion_global': conversion_rate,
        'leads_pending_followup': leads_pending_followup,
        'sources': sources,
        'counts': counts,
        'utilisateurs': [user.username for user in utilisateurs],
        'leads_counts': leads_counts,
        'new_leads_count': new_leads_count,
        'lost_leads_count': lost_leads_count,
        'recent_leads': recent_leads,
    })


# users/views.py
from django.views.generic import ListView
from appointments.models import Appointment
from notifications.models import Notification  # Import the Notification model


class AppointmentsListView(ListView):
    model = Appointment
    template_name = 'appointments_list.html'
# users/views.py
from django.views.generic import ListView
from leads.models import Lead

class LeadActionsView(ListView):
    model = Lead
    template_name = 'lead_actions.html'


def is_admin(user):
    return user.is_staff  # Checks if the user is an admin (staff)
@login_required
@user_passes_test(is_admin)
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()

            # Crée une notification pour tous les utilisateurs
            users = User.objects.all()
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=f'Une nouvelle annonce "{announcement.title}" a été ajoutée.',
                    type='announcement'  # Assurez-vous que ce type est défini dans le modèle Notification
                )
            return redirect('announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'create_announcement.html', {'form': form})




from .models import Announcement  # Assuming you have an Announcement model
from django.shortcuts import render
from .models import Announcement

def announcements_list(request):
    # Récupérer toutes les annonces, triées du plus récent au plus ancien
    announcements = Announcement.objects.all().order_by('-created_at')

    return render(request, 'announcements_list.html', {'announcements': announcements})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement
from .forms import AnnouncementForm
def edit_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Annonce mise à jour avec succès.")
            return redirect('announcements_list')  # Redirige vers la liste des annonces
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'edit_announcement.html', {'form': form, 'announcement': announcement})
def delete_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements_list')
    return render(request, 'delete_announcement.html', {'announcement': announcement})
