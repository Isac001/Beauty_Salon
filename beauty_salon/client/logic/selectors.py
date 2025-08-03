# Django imports.
from django.db.models.query import QuerySet

# Local application imports.
from ..models import Client

# Retrieves all clients from the database.
def client_list() -> QuerySet[Client]:
    return Client.objects.all().order_by('client_name')

# Retrieves a single client by their primary key.
def get_client(*, pk: int) -> Client:
    return Client.objects.get(pk=pk)