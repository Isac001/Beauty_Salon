# Django and project imports.
from django.db.models.query import QuerySet
from ..models import Employee

# Retrieves all employees from the database.
def employee_list() -> QuerySet[Employee]:
    return Employee.objects.all().order_by('employee_name')

# Retrieves a single employee by their primary key.
def get_employee(*, pk: int) -> Employee:
    return Employee.objects.get(pk=pk)