# Django and project imports.
from decimal import Decimal
from ..models import SalonService
from .exceptions import ValidationError

# Creates a new salon service after validating the input data.
def create_salon_service(*, name_of_service: str, value_of_service: Decimal) -> SalonService:

    # List of validation errors.
    errors = []

    # Validate the name of the service.
    if not name_of_service or not name_of_service.strip():
        errors.append('O serviço deve ter um nome.')

    # Check if the value of the service is greater than zero.
    if value_of_service <= Decimal("0.0"):
        errors.append('O valor do serviço deve ser maior que R$ 0,00.')

    # Raises a custom exception if any validation errors are found.
    if errors:
        raise ValidationError(errors)

    # Create a new salon service instance.
    salon_service = SalonService.objects.create(
        name_of_service=name_of_service,
        value_of_service=value_of_service
    )

    # Return the created salon service instance.
    return salon_service

# Updates an existing salon service with new data after validating.
def update_service(*, salon_service: SalonService, data: dict) -> SalonService:

    # List of validation errors.
    errors = []

    # Get the values of the salon service to be updated.
    name_of_service = data.get('name_of_service', salon_service.name_of_service)
    value_of_service = data.get('value_of_service', salon_service.value_of_service)

    # Validate the name of the service.
    if not name_of_service or not name_of_service.strip():
        errors.append('O serviço deve ter um nome.')

    # Check if the value of the service is greater than zero.
    if value_of_service <= Decimal('0.0'):
        errors.append('O valor do serviço não pode ser zerado ou negativo.')
    
    # Raises a custom exception if any validation errors are found.
    if errors:
        raise ValidationError(errors)
    
    # Update the salon service instance.
    salon_service.name_of_service = name_of_service
    salon_service.value_of_service = value_of_service

    # Return the updated salon service instance.
    return salon_service.save()

# Deletes a specific salon service instance.
def delete_service(*, salon_service: SalonService):
    salon_service.delete()