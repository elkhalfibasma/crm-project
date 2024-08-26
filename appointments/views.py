from django.shortcuts import render, get_object_or_404, redirect
from .forms import AppointmentForm
from .models import Appointment
from leads.models import Lead
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta


def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('appointments_list')  # Replace with actual success URL
    else:
        form = AppointmentForm()
    
    # Filter leads based on the current user
    form.fields['lead'].queryset = Lead.objects.filter(Assigné=request.user)
    
    return render(request, 'book_appointment.html', {'form': form})


def appointments_list(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments_list')
    else:
        form = AppointmentForm()
    
    appointments = Appointment.objects.all()
    return render(request, 'appointments_list.html', {'appointments': appointments})

def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})


# View for deleting an appointment
def appointment_delete(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments_list')  # Redirect to the appointment list after successful deletion
    return render(request, 'appointment_confirm_delete.html', {'appointment': appointment})

# View for editing an appointment

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
    
    return render(request, 'book_appointment.html', {'form': form, 'appointment': appointment})