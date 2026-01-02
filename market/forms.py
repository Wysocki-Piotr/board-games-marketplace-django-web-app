from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Listing

class RejestracjaForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adres e-mail")

    class Meta:
        model = User
        fields = ['username', 'email']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['game', 'price', 'condition', 'image']