# Django imports.
from django.db import models

# Defines the Employee data model.
class Employee(models.Model):

    # Field for the employee's name.
    employee_name = models.CharField("Name of Employee",max_length=256, null=False)

    # Field for the employee's email.
    employee_email = models.EmailField("E-mail of Employee",max_length=256, unique=True, null=False)

    # Field for the employee's phone number.
    employee_number = models.CharField("Number of Employee",max_length=20, unique=True, null=False)
    
    # Field for the employee's CPF (Brazilian ID).
    employee_cpf = models.CharField("CPF of Employee",max_length=14, unique=True, null=False)

    # String representation of the model.
    def __str__(self):
        # Returns the employee's name.
        return self.employee_name
    
    # Model metadata options.
    class Meta:
        # Specifies the app label.
        app_label = 'employee'
        # Defines the database table name.
        db_table = 'employee'