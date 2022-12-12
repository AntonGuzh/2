from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import CVModel


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CreateCV(forms.ModelForm):
    class Meta:
        model = CVModel
        fields = [
            'full_name',
            'phone_number',
            'desired_position',
            'photo',
            'email',
            'skills',
            'education',
            'experience'
        ]
