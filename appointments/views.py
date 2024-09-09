from django.shortcuts import render, get_object_or_404, redirect
from .forms import AppointmentForm
from .models import Appointment
from leads.models import Lead
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import calendar


@login_required

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('appointments_list')  # Redirect to the calendar view
    else:
        form = AppointmentForm()
    
    # Filter leads based on the current user
    form.fields['lead'].queryset = Lead.objects.filter(Assigné=request.user)
    
    return render(request, 'book_appointment.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment
from datetime import datetime
from .utils import get_calendar_weeks
  
import random

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
@login_required
def appointments_list(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments_list')
    else:
        form = AppointmentForm()
    
    appointments = Appointment.objects.all()
    
    # Date for the current view (you might need to customize this part)
    today = datetime.now()
    year = today.year
    month = today.month

    # Calculate the number of appointments for each day
    appointment_counts = {day: [] for day in range(1, 32)}  # Initialize with empty lists for each day
    for appointment in appointments:
        day = appointment.date.day
        if day in appointment_counts:
            appointment_counts[day].append(appointment)

    # French month names
    months_fr = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    current_month_name = months_fr[month - 1]

    # Get calendar weeks for the month
    calendar_weeks = get_calendar_weeks(year, month)

    context = {
        'form': form,
        'appointments': appointments,
        'appointment_counts': appointment_counts,
        'year': year,
        'month': month,
        'current_month_name': current_month_name,
        'today': today,
        'calendar_weeks': calendar_weeks,
    }
    
    return render(request, 'appointments_list.html', context)

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_delete(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments_list')  # Redirect to the appointment list after successful deletion
    return render(request, 'appointment_confirm_delete.html', {'appointment': appointment})

# View for editing an appointment

@login_required
def appointment_edit(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le rendez-vous a été modifié avec succès.')
            return redirect('appointments_list')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'book_appointment.html', {'form': form, 'appointment':appointment})
