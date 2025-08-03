# Django and projects imports.
from django import forms

# Form for user login.
class LoginForm(forms.Form):

    # Field for the user's email.
    useremail = forms.CharField(max_length=150)

    # Field for the user's password, using a password input widget.
    password = forms.CharField(widget=forms.PasswordInput)