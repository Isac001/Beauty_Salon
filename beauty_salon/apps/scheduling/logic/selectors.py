# Django imports.
from django.db.models import Q
from django.db.models.query import QuerySet

# Project imports.
from ..models import Scheduling

# Defines a function to get a single scheduling.
def get_scheduling(*, pk: int) -> Scheduling:
    # Retrieves a single scheduling by its primary key.
    return Scheduling.objects.get(pk=pk)

# Defines a function to check for active schedulings.
def client_has_active_scheduling(*, client_id: int) -> bool:
    # Checks if a client has any active (Scheduled or Executing) schedulings.
    return Scheduling.objects.filter(
        client_id=client_id,
        status__in=['Agendado', 'Executando']
    ).exists()

# --- List Functions for Views ---

# Defines a function to list scheduled and canceled items.
def list_scheduled_and_canceled() -> QuerySet[Scheduling]:
    # Retrieves all schedulings with 'Scheduled' or 'Canceled' status.
    return Scheduling.objects.filter(
        Q(status='Agendado') | Q(status='Cancelado')
    ).order_by('date', 'time')

# Defines a function to list completed and executing items.
def list_completed_and_executing() -> QuerySet[Scheduling]:
    # Retrieves all schedulings with 'Completed' or 'Executing' status.
    return Scheduling.objects.filter(
        Q(status='Concluído') | Q(status='Executando')
    ).order_by('date', 'time')

# Defines a function to list only completed items, with an optional date filter.
def list_completed_only(*, date: str = None) -> QuerySet[Scheduling]:
    # Retrieves only schedulings with 'Completed' status, optionally filtered by date.
    
    # Starts the query by filtering for 'Completed' status.
    queryset = Scheduling.objects.filter(status='Concluído')
    
    # Checks if a date was provided.
    if date:
        # If so, applies the date filter to the queryset.
        queryset = queryset.filter(date=date)
        
    # Orders the final queryset and returns it.
    return queryset.order_by('date', 'time')