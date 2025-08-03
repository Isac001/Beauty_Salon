# Django impots.
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

# Project imports.
from .services import login_user
from .forms import LoginForm

# View for handling user login and logout.
class LoginView(View):

    # Handles GET requests to display the login form.
    def get(self, request):
        form = LoginForm()
        return render(request, 'login/login_form.html', {'form': form})
    
    # Handles POST requests for form submission and user authentication.
    def post(self, request):

        # Creates a form instance with the submitted data.
        form = LoginForm(request.POST)

        # Validates the form data.
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticates the user by calling the service function.
            if login_user(request=request, username=username, password=password):
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('home')
            
            # Displays an error message if authentication fails.
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        
        # Renders the template with the form.
        return render(request, 'registration/login.html', {'form': form})