# Django and project imports.
from django import forms
from .models import Scheduling

# Form to handle Scheduling creation and updates.
class SchedulingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If the form is for updating an existing instance, disable the client field.
        if self.instance and self.instance.pk:
            self.fields['client'].disabled = True

    class Meta:
        # Link the form to the Scheduling model.
        model = Scheduling
        
        # Define user-editable fields.
        fields = ['professional', 'client', 'salon_service', 'date', 'time', 'status']

        # Add widgets for better user experience.
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class SchedulingStatusForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['status']