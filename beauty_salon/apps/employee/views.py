# Django imports.
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator

# Local application imports.
from .forms import EmployeeForm
from .logic import selectors, services
from .logic.exceptions import ValidationError 

# Handles the display and pagination of the employee list.
class EmployeeListView(View):

    # Fetches all employees and paginates them.
    def get(self, request):

        # Fetch all employees via the selector.
        all_employees = selectors.employee_list()
        
        # Paginate the results, showing 9 employees per page.
        paginator = Paginator(all_employees, 9) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Pass the page object to the template.
        context = {'page_obj': page_obj}

        # Render the template.
        return render(request, 'employee/employee_list.html', context)

# Handles the creation of a new employee.
class EmployeeCreateView(View):

    # Displays an empty form.
    def get(self, request):

        form = EmployeeForm()

        return render(request, 'employee/employee_form.html', {'form': form})
    
    # Processes the submitted form data.
    def post(self, request):

        # Create a form instance and populate it with data from the request.
        form = EmployeeForm(request.POST)

        if form.is_valid():

            try:

                # Call the service to handle business logic and creation.
                services.employee_create(**form.cleaned_data)
                # Código corrigido
                return redirect('employee:employee-list')            
            except ValidationError as e:

                # If business logic fails, add errors to the form.
                for error_message in e.errors:
                    form.add_error(None, error_message)

        return render(request, 'employee/employee_form.html', {'form': form})

# Handles updating an existing employee.
class EmployeeUpdateView(View):

    # Displays the form pre-filled with existing employee data.
    def get(self, request, pk: int):

        # Initialize the form with the existing employee data.
        employee = selectors.get_employee(pk=pk)
        form = EmployeeForm(instance=employee)

        # Render the template with the form.
        return render(request, 'employee/employee_update.html', {'form': form})

    # Processes the submitted form for an existing employee.
    def post(self, request, pk: int):

        employee = selectors.get_employee(pk=pk)

        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():

            try:

                # Call the service to handle business logic and updates.
                services.employee_update(employee=employee, data=form.cleaned_data)

                # Código corrigido
                return redirect('employee:employee-list')
            except ValidationError as e:

                # If business logic fails, add errors to the form.
                for error_message in e.errors:
                    form.add_error(None, error_message)

        # Render the template with the updated form.   
        return render(request, 'employee/employee_update.html', {'form': form})

# Handles the deletion of a employee.
class EmployeeDeleteView(View):

    # Handles the POST request to delete a employee for security.
    def post(self, request, pk: int):

        # Call the service to handle business logic and deletion.
        employee = selectors.get_employee(pk=pk)

        services.employee_delete(employee=employee)

        return redirect('employee:employee-list')