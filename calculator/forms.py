from django import forms
from .subnet_calculator import *
from django.core.validators import RegexValidator

class CalculatorForm(forms.Form):
    CLASS_CHOICES = (('Any','Any'),('A','A'),('B','B'),('C','C'))
    SUBNET_CHOICES = create_subnet('Any')
    network_class = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'this.form.submit()'}), choices=CLASS_CHOICES)
    subnet = forms.ChoiceField(choices=SUBNET_CHOICES)
    ip_address = forms.CharField(initial='0.0.0.0',validators=[RegexValidator(
            regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
            message='IP Address is not a valid.'
        )])
    def __init__(self, subnet_choices, *args, **kwargs):
        super(CalculatorForm, self).__init__(*args, **kwargs)
        self.fields['subnet'].choices = subnet_choices