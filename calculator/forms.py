from django import forms
from django.core.validators import RegexValidator

NETWORK_CLASS_CHOICES = (('default', 'Please Select a network class'),
                         ('Any', 'Any'), ('A', 'A'), ('B', 'B'), ('C', 'C'),)


class CalculatorForm(forms.Form):
    network_class = forms.ChoiceField(choices=NETWORK_CLASS_CHOICES)
    subnet = forms.ChoiceField(choices=())
    ip_address = forms.CharField(initial='0.0.0.0', validators=[RegexValidator(
        regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
        message='IP Address is not a valid.'
    )])

    def __init__(self, subnet_choices, *args, **kwargs):
        super(CalculatorForm, self).__init__(*args, **kwargs)
        self.fields['subnet'].choices = subnet_choices

    def clean_network_class(self):
        network_class = self.cleaned_data.get('network_class')
        if network_class == 'default':
            raise forms.ValidationError("Please select network class")
        return self.cleaned_data
