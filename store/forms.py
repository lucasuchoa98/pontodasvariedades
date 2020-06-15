from allauth.account.forms import SignupForm
from django import forms
from django.forms import ModelForm
from .models import Contato
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class ContactForm(ModelForm):
    class Meta:
        model = Contato
        fields = ('contact_name', 'contact_email','subject','content',)
        labels = {'contact_name':'Seu nome',
        'contact_email':'Seu email',
        'subject':'Assunto',
        'content':'Mensagem'
        }