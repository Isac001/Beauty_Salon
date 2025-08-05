# Python imports
from datetime import date, time
from django.utils import timezone
from django.db import transaction

# Project imports
from ..models import Scheduling
from . import selectors
from .exceptions import ValidationError

# Scheduling creation
def scheduling_create(
    *, 
    client_id: int, 
    professional_id: int, 
    salon_service_id: int, 
    date: date, 
    time: time
) -> Scheduling:
    
    errors = []

    # Rule: A client can only have one active scheduling
    if selectors.client_has_active_scheduling(client_id=client_id):
        errors.append("This client already has an active scheduling (Scheduled or In Progress).")

    # Rule: Cannot schedule for past dates
    if date < timezone.now().date():
        errors.append("Appointments cannot be created on past dates.")

    if errors:
        raise ValidationError(errors)

    scheduling = Scheduling.objects.create(
        client_id=client_id,
        professional_id=professional_id,
        salon_service_id=salon_service_id,
        date=date,
        time=time,
        status='Agendado'
    )

    return scheduling

@transaction.atomic
def scheduling_update(
    *,
    scheduling: Scheduling,
    data: dict
) -> Scheduling:
    
    # Initialize the error list
    errors = [] 

    # Update all valid fields, except for client_id
    for field, value in data.items():
        if field == 'client_id':
            # This field cannot be changed
            continue
        setattr(scheduling, field, value)

    scheduling.save()
    
    return scheduling


# Scheduling cancellation
@transaction.atomic
def scheduling_cancel(*, scheduling: Scheduling) -> Scheduling:
    errors = []

    # Can only cancel if 'Scheduled' or 'In Progress'
    if scheduling.status not in ['Agendado', 'Executando']:
        errors.append("This scheduling is already in a final state and cannot be canceled.")

    if errors:
        raise ValidationError(errors)

    scheduling.status = 'Cancelado'
    scheduling.save()
    
    return scheduling