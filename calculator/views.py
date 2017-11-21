from django.shortcuts import render
from .forms import CalculatorForm
from .subnet_calculation import *
from django.http import HttpResponse
# Create your views here.

def calculator(request):
    CD = CreateData()
    if request.method == 'GET' and 'network_class' in request.GET:
        network_class = request.GET.get('network_class', None)
        subnet_choices = CD.get_subnet(network_class)
        form = CalculatorForm(subnet_choices)
        form = str(form)
        form = form.split('</tr>')[1].split('<td>')[1].split('</td>')[0].replace('name="subnet"','name="subnet" class="form-control"')
        return HttpResponse(form)
      
    elif request.method == 'POST':
        network_class = request.POST['network_class']
        subnet_choices = CD.get_subnet('default')
        form = CalculatorForm(subnet_choices,request.POST) 
        if form.is_valid():
            # subnet_mask_req = request.POST['subnet']
            # ip_address = request.POST['ip_address']
            # subnet_mask = subnet_mask_req.split('/')[0]
            # network_address = masking(ip_address, subnet_mask)
            # wildcard_mask = subnet2wildcard(subnet_mask)
            # broadcast_address = broadcast_address_is(ip_address, wildcard_mask)
            # binary_subnet_mask = bin_subnet(subnet_mask)
            # host_ip_range = host_ip_range_is(network_address ,broadcast_address)
            # ip_class = ip_class_is(ip_address)
            # cidr_notation = '/' + subnet_mask_req.split('/')[1]
            # cidr_num = subnet_mask_req.split('/')[1]
            # number_of_host = "{:,}".format(number_of_host_is(cidr_num))
            # number_of_usable_host = "{:,}".format(
            #     max(0, number_of_host_is(cidr_num) - 2))
            # ip_type = ip_type_is(ip_address)
            # short = ip_address + ' ' + cidr_notation
            # binary_id = ip2bin_id(ip_address)
            # integer_id = bin_id2int_id(binary_id)
            # hex_id = int_id2hex_id(integer_id)
            # data = {'ip_address': ip_address, 'network_address': network_address,
            #         'host_ip_range': host_ip_range, 'broadcast_address': broadcast_address,
            #         'number_of_host': number_of_host, 'number_of_usable_host': number_of_usable_host,
            #         'subnet_mask': subnet_mask, 'wildcard_mask': wildcard_mask,
            #         'binary_subnet_mask': binary_subnet_mask, 'ip_class': ip_class,
            #         'cidr_notation': cidr_notation, 'ip_type': ip_type,
            #         'short': short, 'binary_id': binary_id,
            #         'integer_id': integer_id, 'hex_id': hex_id,
            #         }
            return render(request, 'calculator.html', {'form': form, 'data': data})
        else:
            subnet_choices = CD.get_subnet(network_class)
            form = CalculatorForm(subnet_choices, request.POST)
            return render(request, 'calculator.html', {'form': form})
    else:    
        subnet_choices = CD.get_subnet('default')
        form = CalculatorForm(subnet_choices,initial={'ip_address':'0.0.0.0'}) 
        return render(request, 'calculator.html', {'form': form})

