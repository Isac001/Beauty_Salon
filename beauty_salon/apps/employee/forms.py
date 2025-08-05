# Django and Python imports.
from django import forms
from .models import Employee

# Form to handle Employee creation and updates.
class EmployeeForm(forms.ModelForm):

    # Meta class to configure the form.
    class Meta:
        
        # Link the form to the Employee model.
        model = Employee
        
        # Define user-editable fields.
        fields = ['employee_name', 'employee_email', 'employee_number', 'employee_cpf']