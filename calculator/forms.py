from django import forms
from .subnet_calculator import *
from django.core.validators import RegexValidator


class CalculatorForm(forms.Form):
    network_class = forms.ChoiceField(choices=())
    subnet = forms.ChoiceField(choices=())
    ip_address = forms.CharField(initial='0.0.0.0', validators=[RegexValidator(
        regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
        message='IP Address is not a valid.'
    )])

    def __init__(self, subnet_choices, class_choices, *args, **kwargs):
        super(CalculatorForm, self).__init__(*args, **kwargs)
        self.fields['subnet'].choices = subnet_choices
        self.fields['network_class'].choices = class_choices
