# Django imports.
from django.db import models
from django.db.models import Q

# Project imports.
from apps.client.models import Client
from apps.employee.models import Employee
from apps.salon_service.models import SalonService

# A list of possible statuses for a scheduling.
STATUS_CHOICES = (
    ("Agendado", "Agendado"),
    ("Concluído", "Concluído"),
    ("Executando", "Executando"),
    ("Cancelado", "Cancelado"),
)

# Defines the Scheduling data model.
class Scheduling(models.Model):

    # FK of the client that will receive the service.
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='schedulings',
        verbose_name='Cliente'
    )

    # FK of the employee that will perform the service.
    professional = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name='schedulings',
        verbose_name='Profissional',
        null=True
    )

    # FK of the salon service that will be performed.
    salon_service = models.ForeignKey(
        SalonService,
        on_delete=models.CASCADE,
        related_name='schedulings',
        verbose_name='Serviço'
    )

    # Date and time of the scheduling.
    date = models.DateField("Data", null=False)
    time = models.TimeField("Horário", null=False)

    # Status of the scheduling.
    status = models.CharField(   
        max_length=20,
        choices=STATUS_CHOICES,
        default="Agendado",
        verbose_name='Status do Agendamento'
    )

    # String representation of the model.
    def __str__(self):
        return f"Scheduling for {self.client.client_name} with {self.professional.employee_name} at {self.date} {self.time}"

    # Model metadata options.
    class Meta:
        app_label = 'scheduling'
        db_table = 'scheduling'
        
        # Ensures a client can only have one active scheduling at a time.
        # An active scheduling is one that is NOT 'Completed' or 'Canceled'.
        constraints = [
            models.UniqueConstraint(
                fields=['client'],
                condition=~Q(status__in=['Concluído', 'Cancelado']),
                name='unique_active_scheduling_per_client'
            )
        ]