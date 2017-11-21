from django import forms
from django.core.validators import RegexValidator
from django.forms.fields import ChoiceField

NETWORK_CLASS_CHOICES = (('default', 'Please Select a network class'), ('Any', 'Any'), ('A', 'A'), ('B', 'B'), ('C', 'C'),)

class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass
        
class CalculatorForm(forms.Form):
    network_class = ChoiceFieldNoValidation(choices=NETWORK_CLASS_CHOICES)
    subnet = ChoiceFieldNoValidation(choices=())
    ip_address = forms.CharField(initial='0.0.0.0', validators=[RegexValidator(
        regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
        message='IP Address is not a valid.'
    )])

    def __init__(self, subnet_choices, *args, **kwargs):
        super(CalculatorForm, self).__init__(*args, **kwargs)
        self.fields['subnet'].choices = subnet_choices
