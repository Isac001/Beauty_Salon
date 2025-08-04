# Django and project imports
from django import forms
from .models import SalonService

# Form for creating and updating SalonService instances.
class SalonServiceForm(forms.ModelForm):

    # Meta class for configuring the form.
    class Meta:

        # Specifies the model this form is based on.
        model = SalonService
        
        # Defines the fields to be included in the form.
        fields = ['name_of_service', 'value_of_service']

        # Custom labels for the form fields.
        labels = {
            'name_of_service': 'Nome do Serviço',
            'value_of_service': 'Valor do Serviço',
        }

        # Specifies custom widgets and their attributes for form fields.
        widgets = {
            'value_of_service': forms.NumberInput(attrs={
                'type': 'number',        
                'step': '0.01',        
                'placeholder': 'R$ 0.00'
            }),
        }