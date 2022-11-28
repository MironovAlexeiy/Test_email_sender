from django import forms
from .models import User
from django.contrib.auth import authenticate


class UserCreationForm(forms.Form):

    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': "inputUsername"
    }))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': "inputUsername"
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': "inputUsername"
    }))
    birth_day = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'id': "inputUsername"
    }))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'inputPassword',
    }))
    rep_password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'ReInputPassword'
    }))

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['rep_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords did not match, please try again.')

    def save(self):
        del self.cleaned_data['rep_password']
        user = User(username=self.cleaned_data['email'],
                    email=self.cleaned_data['email'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    birth_day=self.cleaned_data['birth_day'],)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class SignUser(forms.Form):
    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'inputEmail',
        'placeholder': 'Email'
    }))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control mt-2',
        'id': 'inputPassword',
        'placeholder': 'Password'
    }))