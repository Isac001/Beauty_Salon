# Django and project imports.
from django.db.models.query import QuerySet
from ..models import SalonService

# Retrieves a list of all salon services, ordered by their name.
def salon_service_list() -> QuerySet[SalonService]:
    return SalonService.objects.all().order_by('name_of_service')

# Retrieves a single salon service by its primary key (pk).
def get_salon_service(*, pk: int) -> SalonService:
    return SalonService.objects.get(pk=pk)