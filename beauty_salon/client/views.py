
# Django imports.
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator

# Local application imports.
from .forms import ClientForm
from .logic import selectors, services
from .logic.exceptions import ValidationError  

# Handles the display and pagination of the client list.
class ClientListView(View):

    def get(self, request):

        # Fetch all clients via the selector.
        all_clients = selectors.client_list()
        
        # Paginate the results, showing 10 clients per page.
        paginator = Paginator(all_clients, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Pass the page object to the template.
        context = {'page_obj': page_obj}

        # Render the template.
        return render(request, 'client/client_list.html', context)

# Handles the creation of a new client.
class ClientCreateView(View):

    # Displays an empty form.
    def get(self, request):

        form = ClientForm()

        return render(request, 'client/client_form.html', {'form': form})
    
    # Processes the submitted form data.
    def post(self, request):

        # Create a form instance and populate it with data from the request.
        form = ClientForm(request.POST)

        if form.is_valid():

            try:

                # Call the service to handle business logic and creation.
                services.client_create(**form.cleaned_data)
                return redirect('client-list') 
            
            except ValidationError as e:

                # If business logic fails, add errors to the form.
                for error_message in e.errors:
                    form.add_error(None, error_message)

        return render(request, 'client/client_form.html', {'form': form})

# Handles updating an existing client.
class ClientUpdateView(View):

    # Displays the form pre-filled with existing client data.
    def get(self, request, pk: int):

        # Initialize the form with the existing client data.
        client = selectors.get_client(pk=pk)
        form = ClientForm(instance=client)

        # Render the template with the form.
        return render(request, 'client/client_update.html', {'form': form})

    # Processes the submitted form for an existing client.
    def post(self, request, pk: int):

        client = selectors.get_client(pk=pk)

        form = ClientForm(request.POST, instance=client)

        if form.is_valid():

            try:

                # Call the service to handle business logic and updates.
                services.client_update(client=client, data=form.cleaned_data)

                return redirect('client-list')
            except ValidationError as e:

                # If business logic fails, add errors to the form.
                for error_message in e.errors:
                    form.add_error(None, error_message)

        # Render the template with the updated form.   
        return render(request, 'client/client_update.html', {'form': form})

# Handles the deletion of a client.
class ClientDeleteView(View):

    # Handles the POST request to delete a client for security.
    def post(self, request, pk: int):

        # Call the service to handle business logic and deletion.
        client = selectors.get_client(pk=pk)

        services.client_delete(client=client)

        return redirect('client-list')