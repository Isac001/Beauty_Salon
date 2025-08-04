# Python imports.
import re

# Local application imports.
from ..models import Client
from .exceptions import ValidationError

# Define allowed email domains for validation.
ALLOWED_DOMAINS = ["gmail", "hotmail", "outlook"]

# Handles the business logic for creating a new client.
def client_create(*, client_name: str, client_email: str, client_number: str) -> Client:
    # A list to aggregate validation errors.
    errors = []
    
    # Sanitize phone number to contain only digits for validation.
    cleaned_number = re.sub(r'\D', '', client_number)


    # Check if the client's name is a full name (at least two words).
    if len(client_name.strip().split()) < 2:
        errors.append("O nome do cliente deve ser completo.")
    
    # Check if the phone number has the correct amount of digits.
    if len(cleaned_number) != 11:
        errors.append("O número de telefone deve ter 11 dígitos (ex: (XX) XXXXX-XXXX).")
    
    # Check if the email domain is in the allowed list.
    try: 
        domain_part = client_email.split('@')[1]
        main_domain = domain_part.split('.')[0]
        if main_domain.lower() not in ALLOWED_DOMAINS:
            errors.append(f"O domínio '{main_domain}' não é permitido. Use gmail, hotmail ou outlook.")
    # Catches emails without an '@' symbol.
    except IndexError:
        errors.append("Formato de E-mail inválido.")
    
    # Check if the email is already in use.
    if Client.objects.filter(client_email=client_email).exists():
        errors.append("Este e-mail já está em uso.")

    # If any validation failed, raise an exception with the full list of errors.
    if errors:
        raise ValidationError(errors)
    
    # Reformat the cleaned number to a standard presentation format.
    formatted_number = f"({cleaned_number[0:2]}) {cleaned_number[2:7]}-{cleaned_number[7:11]}"
    
    # If all validations pass, create the new client.
    client = Client.objects.create(
        client_name=client_name,
        client_email=client_email,
        client_number=formatted_number
    )
    return client

# Handles the business logic for updating an existing client.
def client_update(*, client: Client, data: dict) -> Client:

    # A list to aggregate validation errors.
    errors = []

    # Safely retrieve new data from the input dictionary.
    client_name = data.get('client_name', client.client_name)
    client_email = data.get('client_email', client.client_email)
    client_number = data.get('client_number', client.client_number)

    # Sanitize phone number to contain only digits for validation.
    cleaned_number = re.sub(r'\D', '', client_number)
    
    # Check if the client's name is a full name (at least two words).
    if len(client_name.strip().split()) < 2:
        errors.append("O nome do cliente deve ser completo.")

    # Check if the phone number has the correct amount of digits.
    if len(cleaned_number) != 11:
        errors.append("O número de telefone deve ter 11 dígitos.")

    # Check if the email domain is in the allowed list.
    try:
        domain_part = client_email.split('@')[1]
        main_domain = domain_part.split('.')[0]
        if main_domain.lower() not in ALLOWED_DOMAINS:
            errors.append(f"O domínio '{main_domain}' não é permitido. Use gmail, hotmail ou outlook.")
    # Catches emails without an '@' symbol.
    except IndexError:
        errors.append("Formato de E-mail inválido.")
    
    # Check if the email is already in use by another client.
    if Client.objects.filter(client_email=client_email).exclude(pk=client.pk).exists(): 
        errors.append("Este E-mail já está cadastrado por outro cliente.")

    # If any validation failed, raise an exception with the full list of errors.
    if errors:
        raise ValidationError(errors)
    
    # Reformat the cleaned number to a standard presentation format.
    formatted_number = f"({cleaned_number[0:2]}) {cleaned_number[2:7]}-{cleaned_number[7:11]}"
    
    # If validations pass, update the client instance fields.
    client.client_name = client_name
    client.client_email = client_email
    client.client_number = formatted_number
    client.save()

    return client

# Handles the deletion of a client instance.
def client_delete(*, client: Client):
    client.delete()