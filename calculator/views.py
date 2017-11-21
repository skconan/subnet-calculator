from django.shortcuts import render
from .forms import CalculatorForm
from .subnet_calculation import *
from django.http import HttpResponse
import re

def calculator(request):
    CD = CreateData()
    if request.method == 'GET' and 'network_class' in request.GET:
        network_class = request.GET.get('network_class', None)
        subnet_choices = CD.get_subnet(network_class)
        form = CalculatorForm(subnet_choices)
        form = str(form)
        form = form.split('</tr>')[1].split('<td>')[1].split('</td>')[0].replace(
            'name="subnet"', 'name="subnet" class="form-control"')
        return HttpResponse(form)

    elif request.method == 'POST':
        err_ip = False
        err_network_class = False
        
        network_class = request.POST['network_class']
        subnet_mask = request.POST['subnet']
        ip_address = request.POST['ip_address']

        regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    
        if re.match(regex,ip_address) is None:
            err_ip = 'IP Address is not a valid.'
        if network_class == 'default':
            err_network_class = 'Please select a network class'
            
        if not (err_ip or err_network_class):
            SC = SubnetCalculation(network_class, subnet_mask, ip_address)
            data = SC.calculate()
            subnet_choices = CD.get_subnet('default')
            form = CalculatorForm(subnet_choices,
                                initial={'ip_address': ip_address})
            return render(request, 'calculator.html', {'form': form, 'data': data})
        else:
            err = {'err_ip':err_ip,'err_network_class':err_network_class}
            subnet_choices = CD.get_subnet(network_class)
            form = CalculatorForm(subnet_choices, request.POST)
            return render(request, 'calculator.html', {'form': form,'err':err})
    else:
        subnet_choices = CD.get_subnet('default')
        form = CalculatorForm(subnet_choices,
                              initial={'ip_address': '0.0.0.0'})
        return render(request, 'calculator.html', {'form': form})
