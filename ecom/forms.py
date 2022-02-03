from django import forms
from django.conf import settings
# from accounts.models import EmailActivation
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'form_full_name', 'placeholder': 'Your Fullname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'form_email', 'placeholder': 'Email ID'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'form_full_name', 'placeholder': 'Your Fullname'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError('please enter proper email')
        return email
