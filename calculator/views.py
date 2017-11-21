from django.shortcuts import render
from .forms import CalculatorForm
from .subnet_calculation import *
from django.http import HttpResponse


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
        network_class = request.POST['network_class']
        subnet_choices = CD.get_subnet(network_class)
        form = CalculatorForm(subnet_choices, request.POST)
        if form.is_valid():
            subnet_mask = request.POST['subnet']
            ip_address = request.POST['ip_address']

            SC = SubnetCalculation(network_class, subnet_mask, ip_address)
            data = SC.calculate()

            subnet_choices = CD.get_subnet('default')
            form = CalculatorForm(subnet_choices,
                                  initial={'ip_address': ip_address})
            return render(request, 'calculator.html', {'form': form, 'data': data})
        else:
            subnet_choices = CD.get_subnet(network_class)
            form = CalculatorForm(subnet_choices, request.POST)
            return render(request, 'calculator.html', {'form': form})
    else:
        subnet_choices = CD.get_subnet('default')
        form = CalculatorForm(subnet_choices,
                              initial={'ip_address': '0.0.0.0'})
        return render(request, 'calculator.html', {'form': form})
