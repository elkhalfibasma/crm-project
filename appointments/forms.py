from django import forms
from .models import Appointment
from leads.models import Lead

class AppointmentForm(forms.ModelForm):
    LOCATIONS = [
        ('Casablanca', 'Casablanca'),
        ('Rabat', 'Rabat'),
        ('Marrakech', 'Marrakech'),
        ('Fes', 'Fes'),
        ('Tangier', 'Tangier'),
        ('Agadir', 'Agadir'),
        # Add more cities as needed
    ]

    location = forms.ChoiceField(choices=LOCATIONS, required=True)
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datetimepicker'}))

    class Meta:
        model = Appointment
        fields = ['lead', 'date', 'location', 'notes', 'confirmed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Do not handle user here
