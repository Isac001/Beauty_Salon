# Django imports.
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages

# Project imports.
from .forms import SchedulingForm
from .logic import services
from .logic import selectors
from .logic.exceptions import ValidationError
from .models import Scheduling


# View to display a list of scheduled and canceled schedulings.
class ScheduledAndCanceledListView(View):
    """
    Handles the display of a list of scheduled and canceled schedulings.
    """

    def get(self, request):
        """
        Handles GET requests to display the paginated list.
        """
        # Fetches the list of schedulings from the selector.
        scheduling_list = selectors.list_scheduled_and_canceled()

        # Paginates the results, showing 10 items per page.
        paginator = Paginator(scheduling_list, 10)

        # Gets the current page number from the request.
        page_number = request.GET.get('page')

        # Gets the page object for the current page.
        page_obj = paginator.get_page(page_number)

        # Prepares the context data to be sent to the template.
        context = { 'page_obj': page_obj, 'page_title': 'Agendamentos' }

        # Renders the template with the provided context.
        return render(request, 'scheduling/scheduling_seach.html', context)


# View to display a list of completed and executing schedulings.
class CompletedAndExecutingListView(View):
    """
    Handles the display of a list of completed and in-progress schedulings.
    """

    def get(self, request):
        """
        Handles GET requests to display the paginated list.
        """
        # Fetches the list of schedulings from the selector.
        scheduling_list = selectors.list_completed_and_executing()

        # Paginates the results.
        paginator = Paginator(scheduling_list, 10)

        # Gets the current page number.
        page_number = request.GET.get('page')

        # Gets the page object.
        page_obj = paginator.get_page(page_number)

        # Prepares the context.
        context = { 'page_obj': page_obj, 'page_title': 'Acompanhamento' }

        # Renders the template.
        return render(request, 'scheduling/scheduling_seach.html', context)


# View to display a report of completed schedulings only.
class CompletedOnlyListView(View):
    """
    Handles the display of a list of completed schedulings, with an optional date filter.
    """

    def get(self, request):
        """
        Handles GET requests to display the paginated and filtered list.
        """
        # Gets the date from the URL parameters for filtering.
        date_filter = request.GET.get('date')

        # Fetches the filtered list of schedulings.
        scheduling_list = selectors.list_completed_only(date=date_filter)

        # Paginates the results.
        paginator = Paginator(scheduling_list, 4)

        # Gets the current page number.
        page_number = request.GET.get('page')

        # Gets the page object.
        page_obj = paginator.get_page(page_number)

        # Prepares the context.
        context = { 'page_obj': page_obj, 'page_title': 'Relatório de Agendamentos Concluídos' }

        # Renders the template.
        return render(request, 'scheduling/scheduling_seach.html', context)


# View for creating a new scheduling.
class SchedulingCreateView(View):
    """
    Handles the creation of a new scheduling entry.
    """
    
    def get(self, request):
        """
        Handles GET requests by displaying an empty form.
        """
        # Creates an instance of the form.
        form = SchedulingForm()

        # Renders the form template.
        return render(request, 'scheduling/scheduling_form.html', {'form': form})
    
    def post(self, request):
        """
        Handles POST requests with the submitted form data.
        """
        # Binds the form to the POST data.
        form = SchedulingForm(request.POST)

        # Checks if the form is valid.
        if form.is_valid():
            # Tries to create the scheduling using the service layer.
            try:
                # Calls the service function to create the scheduling.
                services.scheduling_create(
                    client_id=form.cleaned_data.get('client').pk,
                    professional_id=form.cleaned_data.get('professional').pk,
                    salon_service_id=form.cleaned_data.get('salon_service').pk,
                    date=form.cleaned_data.get('date'),
                    time=form.cleaned_data.get('time')
                )

                # Redirects to the home page on success.
                return redirect('home:home')
            
            # Catches custom validation errors from the service layer.
            except ValidationError as e:
                # Adds the errors to the form to be displayed to the user.
                for error_message in e.errors:
                    form.add_error(None, error_message)

        # Renders the form again with any error messages.
        return render(request, 'scheduling/scheduling_form.html', {'form': form})


# View for updating an existing scheduling.
class SchedulingUpdateView(View):
    """
    Handles the update of an existing scheduling entry.
    """

    def get(self, request, pk: int):
        """
        Handles GET requests by displaying the form pre-filled with existing data.
        """
        # Fetches the specific scheduling object or returns a 404 error.
        scheduling = get_object_or_404(Scheduling, pk=pk)

        # Creates a form instance bound to the scheduling object.
        form = SchedulingForm(instance=scheduling)

        # Renders the form, passing a flag to indicate it's an update.
        return render(request, 'scheduling/scheduling_form.html', {'form': form, 'is_update': True})

    def post(self, request, pk: int):
        """
        Handles POST requests with the updated form data.
        """
        # Fetches the specific scheduling object.
        scheduling = get_object_or_404(Scheduling, pk=pk)

        # Binds the form to the POST data and the existing instance.
        form = SchedulingForm(request.POST, instance=scheduling)

        # Checks if the form is valid.
        if form.is_valid():
            # Tries to update the scheduling.
            try:
                # Calls the service function to update the data.
                services.scheduling_update(scheduling=scheduling, data=form.cleaned_data)

                # Redirects to the home page on success.
                return redirect('home:home')
            
            # Catches custom validation errors.
            except ValidationError as e:
                # Adds errors to the form.
                for error_message in e.errors:
                    form.add_error(None, error_message)

        # Renders the form again with any errors.
        return render(request, 'scheduling/scheduling_form.html', {'form': form, 'is_update': True})


# View to handle the cancellation of a scheduling.
class SchedulingCancelView(View):
    """
    Handles the cancellation of an existing scheduling.
    """

    def post(self, request, pk: int):
        """
        Handles POST requests to cancel a scheduling.
        """
        # Fetches the specific scheduling object.
        scheduling = get_object_or_404(Scheduling, pk=pk)

        # Tries to cancel the scheduling.
        try:
            # Calls the service function to cancel the scheduling.
            services.scheduling_cancel(scheduling=scheduling)

        # Catches custom validation errors.
        except ValidationError as e:
            # Adds errors to the messages.
            for error_message in e.errors:
                messages.error(request, error_message)
        
        # Redirects to the home page on success.
        return redirect('home:home')