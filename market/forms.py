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
        fields = ['game', 'custom_title', 'price', 'condition', 'image']
        labels = {
            'game': 'Wybierz grę z bazy (opcjonalnie)',
            'custom_title': 'LUB wpisz własną nazwę (jeśli nie ma na liście)',
        }

        widgets = {
            'game': forms.Select(attrs={
                'class': 'select2-game',
                'style': 'width: 100%'
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            game = cleaned_data.get("game")
            custom_title = cleaned_data.get("custom_title")

            if not game and not custom_title:
                raise forms.ValidationError("Musisz wybrać grę z listy LUB wpisać własny tytuł.")

            if game and custom_title:
                raise forms.ValidationError("Wybierz tylko jedną opcję: albo lista, albo własny tytuł.")

            return cleaned_data