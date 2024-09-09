from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from conversations.models import Conversation, Message  # Import the Notification model
@login_required

def notifications_view(request):
    # Récupérer toutes les notifications non lues de l'utilisateur connecté
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Passer le contexte au template
    context = {
        'notifications': notifications,
        'notifications_count': notifications.count(),  # Compter le nombre de notifications non lues
    }
    
    return render(request, 'notifications.html', context)



from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required

def create_notification(user=None, notification_type='announcement', **kwargs):
    # Définir le message de notification en fonction du type
    if notification_type == 'lead':
        lead = kwargs.get('lead')
        message = f"Nouveau lead ajouté : {lead.Prénom} {lead.Nom} le {lead.crée.strftime('%Y-%m-%d %H:%M:%S')}"
        users = User.objects.all()  # Créer une notification pour tous les utilisateurs
    elif notification_type == 'announcement':
        title = kwargs.get('title')
        if kwargs.get('updated', False):
            message = f"L'annonce '{title}' a été mise à jour."
        else:
            message = f"Nouvelle annonce : {title}"
        users = User.objects.all()  # Créer une notification pour tous les utilisateurs
    else:
        message = "Vous avez une nouvelle notification"
        users = [user]

    # Créer des notifications pour chaque utilisateur
    for user in users:
        Notification.objects.create(
            user=user,
            message=message,
            type=notification_type,
            is_read=False
        )


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

