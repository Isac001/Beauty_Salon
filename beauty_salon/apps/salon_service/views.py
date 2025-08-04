
# Django imports.
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator

# Local application imports.
from .forms import SalonServiceForm
from .logic import selectors, services
from .logic.exceptions import ValidationError


# View for displaying a paginated list of all salon services.
class SalonServiceListView(View):

    # Handles GET requests to display the list.
    def get(self, request):

        # Fetch all salon services via the selector.
        all_services = selectors.salon_service_list()

        # Paginate the results, showing 9 services per page.
        paginator = Paginator(all_services, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Pass the page object to the template.
        context = {'page_obj': page_obj}

        # Render the template.
        return render(request, 'salon_service/salon_service_list.html', context)
    
# View for creating a new salon service.
class SalonServiceCreateView(View):

    # Handles GET requests to display the creation form.
    def get(self, request):
        form = SalonServiceForm
        return render(request, 'salon_service/salon_service_form.html', {'form': form})

    # Handles POST requests to submit and validate the form.
    def post(self, request):

        # Creates a form instance with the submitted data.
        form = SalonServiceForm(request.POST)

        # Validates the form data.
        if form.is_valid():

            try:
                # Calls the service function to create the object.
                services.create_salon_service(**form.cleaned_data)

                # CORRIGIDO: usa o namespace da app
                return redirect('salon_service:list-salon-service')
            
            except ValidationError as e:

                # Adds custom validation errors to the form.
                for error_message in e.errors:

                    form.add_error(None, error_message)

        return render(request, 'salon_service/salon_service_form.html', {'form': form})
    
# View for updating an existing salon service.
class SalonServiceUpdateView(View):

    # Handles GET requests to display the update form with pre-filled data.
    def get(self, request, pk: int):
        salon_service = selectors.get_salon_service(pk=pk)
        form = SalonServiceForm(instance=salon_service)
        return render(request, 'salon_service/salon_service_update.html', {'form': form})
    
    # Handles POST requests to submit and validate the updated data.
    def post(self, request, pk: int):

        # Retrieves the object to be updated.
        salon_service = selectors.get_salon_service(pk=pk)
        form = SalonServiceForm(request.POST, instance=salon_service)

        # Validates the form data.
        if form.is_valid():

            try:

                # Calls the service function to update the object.
                services.update_service(salon_service=salon_service, data=form.cleaned_data)

                # CORRIGIDO: usa o namespace da app
                return redirect('salon_service:list-salon-service')
            
            except ValidationError as e:

                # Adds custom validation errors to the form.
                for error_message in e.errors:

                    form.add_error(None, error_message)

        # Renders the template with the updated form.
        return render(request, 'salon_service/salon_service_update.html', {'form': form})
    

# View for deleting a salon service.
class SalonServiceDeleteView(View):

    # Handles POST requests to delete an object.
    def post(self, request, pk: int):

        # Retrieves the object to be deleted.
        salon_service = selectors.get_salon_service(pk=pk)

        # Calls the service function to delete the object.
        services.delete_service(salon_service=salon_service)

        # CORRIGIDO: usa o namespace da app
        return redirect('salon_service:list-salon-service')