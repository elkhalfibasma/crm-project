# leads/forms.py
from django import forms
from .models import Lead
from django.contrib.auth.models import User



class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['Prénom', 'Nom', 'Email', 'Télephone', 'source', 'statut', 'notes']


class LeadImportForm(forms.Form):
    csv_file = forms.FileField()



class AssignLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['Assigné']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Assigné'].queryset = User.objects.all()
from django import forms
from django import forms
from .models import Interaction

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['type', 'details', 'duree', 'commentaires']
        widgets = {
            'type': forms.HiddenInput(),
        }
from django import forms
from .models import Interaction

from django import forms
from .models import Interaction

class AppelForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['date', 'details', 'duree', 'commentaires']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Sélectionnez une date'
            }),
            'details': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Entrez les détails de l\'appel'
            }),
            'duree': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Durée de l\'appel (en minutes)'
            }),
            'commentaires': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Ajoutez des commentaires supplémentaires'
            }),
        }

