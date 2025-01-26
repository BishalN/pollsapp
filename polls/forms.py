from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Poll, Choice

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']