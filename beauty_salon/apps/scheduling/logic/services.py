# Python imports
from datetime import date, time
from django.utils import timezone
from django.db import transaction

# Project imports
from ..models import Scheduling
from . import selectors
from .exceptions import ValidationError

# Criação de agendamento
def scheduling_create(
    *, 
    client_id: int, 
    professional_id: int, 
    salon_service_id: int, 
    date: date, 
    time: time
) -> Scheduling:
    
    errors = []

    # Regra: Cliente só pode ter um agendamento ativo
    if selectors.client_has_active_scheduling(client_id=client_id):
        errors.append("Este cliente já possui um agendamento ativo (Agendado ou Executando).")

    # Regra: Não pode agendar para datas passadas
    if date < timezone.now().date():
        errors.append("Agendamentos não podem ser criados em datas passadas.")

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
    
    errors = [] # Inicializamos a lista de erros

    current_status = scheduling.status
    
    # Regra: Não permitir alteração em agendamentos já em estado final
    if current_status in ['Cancelado', 'Concluído']:
        errors.append('O agendamento está em um estado final e não pode ser alterado.')

    if errors:
        raise ValidationError(errors)
        
    # Atualiza todos os campos válidos, incluindo o status
    for field, value in data.items():
        setattr(scheduling, field, value)

    scheduling.save()
    
    return scheduling


# Cancelamento de agendamento
@transaction.atomic
def scheduling_cancel(*, scheduling: Scheduling) -> Scheduling:
    errors = []

    # Só pode cancelar se estiver 'Agendado' ou 'Executando'
    if scheduling.status not in ['Agendado', 'Executando']:
        errors.append("Este agendamento já está em um estado final e não pode ser cancelado.")

    if errors:
        raise ValidationError(errors)

    scheduling.status = 'Cancelado'
    scheduling.save()
    
    return scheduling