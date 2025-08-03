# Django and project imports.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest


# Authenticates a user with the provided credentials and starts their session.
def login_user(*, request: HttpRequest, username: str, password: str):

    # Authenticates the user with Django's built-in system.
    user = authenticate(request, username=username, password=password)

    # If the user is found and credentials are correct.
    if user is not None:

        # Logs the user in by starting a new session.
        login(request, user)

        # Return True for a successful login.
        return True 
    
    # Return False if authentication fails.
    return False

# Logs out the current user by ending their session.
def logout_user(*, request: HttpRequest):

    # Calls Django's built-in logout function.
    logout(request)