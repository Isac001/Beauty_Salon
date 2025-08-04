# Django and project imports
from django.db import models

# Model representing a service offered by a salon.
class SalonService(models.Model):

    # The name of the service.
    name_of_service = models.CharField("Name of service", max_length=256, null=False)
    
    # The monetary value of the service.
    value_of_service = models.DecimalField("Value of service", max_digits=8,decimal_places=2, null=False)

    # Returns a string representation of the object.
    def __str__(self):
        
        return self.name_of_service
    
    # Model metadata.
    class Meta:

        # Specifies the app label for this model.
        app_label = 'salon_service'

        # Defines the database table name.
        db_table = 'salon_service'