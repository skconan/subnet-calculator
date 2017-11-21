from django import forms
from django.core.validators import RegexValidator

NETWORK_CLASS_CHOICES = (('default', 'Please select a network class'),
                         ('Any', 'Any'), ('A', 'A'), ('B', 'B'), ('C', 'C'),)


class CalculatorForm(forms.Form):
    network_class = forms.ChoiceField(choices=NETWORK_CLASS_CHOICES)
    subnet = forms.ChoiceField(choices=())
    ip_address = forms.CharField(initial='0.0.0.0')

    def __init__(self, subnet_choices, *args, **kwargs):
        super(CalculatorForm, self).__init__(*args, **kwargs)
        self.fields['subnet'].choices = subnet_choices