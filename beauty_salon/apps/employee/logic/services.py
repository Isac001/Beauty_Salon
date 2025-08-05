# Python imports.
import re

# Local application imports.
from ..models import Employee
from .exceptions import ValidationError

# Define allowed email domains for validation.
ALLOWED_DOMAINS = ["gmail", "hotmail", "outlook"]

# Handles the business logic for creating a new employee.
def employee_create(*, employee_name: str, employee_email: str, employee_number: str, employee_cpf: str) -> Employee:
    # A list to aggregate validation errors.
    errors = []
    
    # Sanitize number and cpf to contain only digits for validation.
    cleaned_number = re.sub(r'\D', '', employee_number)
    cleaned_cpf = re.sub(r'\D', '', employee_cpf)


    # Check if the employee's name is a full name (at least two words).
    if len(employee_name.strip().split()) < 2:
        errors.append("O nome do funcionário deve ser completo.")
    
    # Check if the phone number has the correct amount of digits.
    if len(cleaned_number) != 11:
        errors.append("O número de telefone deve ter 11 dígitos (ex: (XX) XXXXX-XXXX).")
    
    # Check if the cpf has the correct amount of digits.
    if len(cleaned_cpf) != 11:
        errors.append("O CPF deve ter 11 dígitos.")
    
    # Check if the email domain is in the allowed list.
    try: 
        domain_part = employee_email.split('@')[1]
        main_domain = domain_part.split('.')[0]
        if main_domain.lower() not in ALLOWED_DOMAINS:
            errors.append(f"O domínio '{main_domain}' não é permitido. Use gmail, hotmail ou outlook.")
    # Catches emails without an '@' symbol.
    except IndexError:
        errors.append("Formato de E-mail inválido.")
    
    # Check if the email is already in use.
    if Employee.objects.filter(employee_email=employee_email).exists():
        errors.append("Este e-mail já está em uso.")

    # Check if the number is already in use.
    if Employee.objects.filter(employee_number=employee_number).exists():
        errors.append("Este número já está em uso.")
    
    # Check if the cpf is already in use.
    if Employee.objects.filter(employee_cpf=employee_cpf).exists():
        errors.append("Este CPF já está em uso.")

    # If any validation failed, raise an exception with the full list of errors.
    if errors:
        raise ValidationError(errors)
    
    # Reformat the cleaned number and cpf to a standard presentation format.
    formatted_number = f"({cleaned_number[0:2]}) {cleaned_number[2:7]}-{cleaned_number[7:11]}"
    formatted_cpf = f"{cleaned_cpf[0:3]}.{cleaned_cpf[3:6]}.{cleaned_cpf[6:9]}-{cleaned_cpf[9:11]}"
    
    # If all validations pass, create the new employee.
    employee = Employee.objects.create(
        employee_name=employee_name,
        employee_email=employee_email,
        employee_number=formatted_number,
        employee_cpf=formatted_cpf
    )
    return employee

# Handles the business logic for updating an existing employee.
def employee_update(*, employee: Employee, data: dict) -> Employee:

    # A list to aggregate validation errors.
    errors = []

    # Safely retrieve new data from the input dictionary.
    employee_name = data.get('employee_name', employee.employee_name)
    employee_email = data.get('employee_email', employee.employee_email)
    employee_number = data.get('employee_number', employee.employee_number)
    employee_cpf = data.get('employee_cpf', employee.employee_cpf)

    # Sanitize number and cpf to contain only digits for validation.
    cleaned_number = re.sub(r'\D', '', employee_number)
    cleaned_cpf = re.sub(r'\D', '', employee_cpf)
    
    # Check if the employee's name is a full name (at least two words).
    if len(employee_name.strip().split()) < 2:
        errors.append("O nome do funcionário deve ser completo.")

    # Check if the phone number has the correct amount of digits.
    if len(cleaned_number) != 11:
        errors.append("O número de telefone deve ter 11 dígitos.")
    
    # Check if the cpf has the correct amount of digits.
    if len(cleaned_cpf) != 11:
        errors.append("O CPF deve ter 11 dígitos.")

    # Check if the email domain is in the allowed list.
    try:
        domain_part = employee_email.split('@')[1]
        main_domain = domain_part.split('.')[0]
        if main_domain.lower() not in ALLOWED_DOMAINS:
            errors.append(f"O domínio '{main_domain}' não é permitido. Use gmail, hotmail ou outlook.")
    # Catches emails without an '@' symbol.
    except IndexError:
        errors.append("Formato de E-mail inválido.")
    
    # Check if the email is already in use by another employee.
    if Employee.objects.filter(employee_email=employee_email).exclude(pk=employee.pk).exists(): 
        errors.append("Este E-mail já está cadastrado por outro funcionário.")
    
    # Check if the number is already in use by another employee.
    if Employee.objects.filter(employee_number=employee_number).exclude(pk=employee.pk).exists(): 
        errors.append("Este número já está cadastrado por outro funcionário.")
    
    # Check if the cpf is already in use by another employee.
    if Employee.objects.filter(employee_cpf=employee_cpf).exclude(pk=employee.pk).exists(): 
        errors.append("Este CPF já está cadastrado por outro funcionário.")

    # If any validation failed, raise an exception with the full list of errors.
    if errors:
        raise ValidationError(errors)
    
    # Reformat the cleaned number and cpf to a standard presentation format.
    formatted_number = f"({cleaned_number[0:2]}) {cleaned_number[2:7]}-{cleaned_number[7:11]}"
    formatted_cpf = f"{cleaned_cpf[0:3]}.{cleaned_cpf[3:6]}.{cleaned_cpf[6:9]}-{cleaned_cpf[9:11]}"
    
    # If validations pass, update the employee instance fields.
    employee.employee_name = employee_name
    employee.employee_email = employee_email
    employee.employee_number = formatted_number
    employee.employee_cpf = formatted_cpf
    employee.save()

    return employee

# Handles the deletion of a employee instance.
def employee_delete(*, employee: Employee):
    employee.delete()