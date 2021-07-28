from django import forms
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm

class MyPwdChForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Régi jelszó",
        strip=True,
        widget=forms.PasswordInput,
        help_text="\n",
    )
    new_password1 = forms.CharField(
        label="Új jelszó",
        strip=True,
        widget=forms.PasswordInput,
        help_text="\n", 
    )
    new_password2 = forms.CharField(
        label="Új jelszó megismétlése",
        strip=True,
        widget=forms.PasswordInput,
    )

class MyAuthForm(AuthenticationForm):
    username = forms.CharField(
        label="Felhasználónév",
        strip=True,
        widget=forms.TextInput,
        help_text="\n",
    )
    password = forms.CharField(
        label="Jelszó",
        strip=True,
        widget=forms.PasswordInput,
        help_text="\n", 
    )

class AllomasAddForm(forms.Form):
    allomasnev = forms.CharField(
        max_length=50,
        required=True,
        strip=True,
        label='Állomásnév',
        help_text="\n",
    )
    vonalszam = forms.CharField(
        max_length=3,
        required=True,
        strip=True,
        label='Vonalszám',
        help_text="\n",
    )

class VonalAddForm(forms.Form):
    vonalszam = forms.CharField(
        max_length=3,
        required=True,
        strip=True,
        label='Vonalszám',
        help_text="\n",
    )
    kezdo_allomas = forms.CharField(
        max_length=50,
        strip=True,
        label='Kezdő állomás',
        help_text="\n",
    )
    vegallomas = forms.CharField(
        max_length=50,
        strip=True,
        label='Végállomás',
        help_text="\n",
    )

class SearchForm(forms.Form):
    allomas = forms.CharField(max_length=75, required=False)
    allomaskoz = forms.CharField(max_length=100, required=False)
    szelvenyszam = forms.CharField(max_length=20, required=False)
    vonal = forms.CharField(max_length=3, required=False)
    egyseg = forms.CharField(max_length=25, required=False)
    dokumentum = forms.CharField(max_length=50, required=False)
