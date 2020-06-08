from allauth.account.forms import SignupForm
from django import forms
from .models import *

class CustomSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)



        # You must return the original result.
        return user