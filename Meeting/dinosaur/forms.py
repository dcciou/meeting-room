from django import forms
from django.contrib.auth.models import User
from .models import Order

class Logi_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class Register_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]


class Add_form(forms.ModelForm):
    time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M:%S%z'],  # 包括时区信息
    )

    class Meta:
        model = Order
        fields = [
            'time',
        ]

class EventForm(forms.Form):
    title = forms.CharField(max_length=100, label='Event Title')
    description = forms.CharField(widget=forms.Textarea, label='Event Description')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'datetime-local'}), label='Event Date and Time')
