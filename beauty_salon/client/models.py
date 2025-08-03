
# Django imports.
from django.db import models

# Defines the Client data model.
class Client(models.Model):

    # Fields of the model.
    client_name = models.CharField("Nome do Cliente", max_length=256)
    client_email = models.EmailField("E-mail", max_length=256, unique=True)
    client_number = models.CharField("Número do Cliente", max_length=20)

    # String representation of the model.
    def __str__(self):
        return self.client_name
    
    # Model metadata options.
    class Meta:

        # Specifies the app label.
        app_label = 'client'
        
        # Defines the database table name.
        db_table = 'client'