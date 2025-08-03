# Django and Python imports.
from django import forms
from .models import Client

# Form to handle Client creation and updates

class ClientForm(forms.ModelForm):
    class Meta:
        
        # Link the form to the Client model.
        model = Client
        
        # Define user-editable fields.
        fields = ['client_name', 'client_email', 'client_number']