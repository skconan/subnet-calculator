from django.shortcuts import render
from .forms import CalculatorForm
from .subnet_calculator import *
# Create your views here.


def calculator(request):
    if request.method == 'POST':
        network_class = request.POST['network_class']
        form = CalculatorForm(create_subnet(network_class), request.POST)
        if form.is_valid():
            subnet_mask_req = request.POST['subnet']
            ip_address = request.POST['ip_address']
            subnet_mask = subnet_mask_req.split('/')[0]
            network_address = masking(ip_address, subnet_mask)
            wildcard_mask = subnet2wildcard(subnet_mask)
            broadcast_address = broadcast_address_is(ip_address, wildcard_mask)
            binary_subnet_mask = bin_subnet(subnet_mask)
            host_ip_range = host_ip_range_is(network_address ,broadcast_address)
            ip_class = ip_class_is(ip_address)
            cidr_notation = '/' + subnet_mask_req.split('/')[1]
            cidr_num = subnet_mask_req.split('/')[1]
            number_of_host = "{:,}".format(number_of_host_is(cidr_num))
            number_of_usable_host = "{:,}".format(
                max(0, number_of_host_is(cidr_num) - 2))
            ip_type = ip_type_is(ip_address)
            short = ip_address + ' ' + cidr_notation
            binary_id = ip2bin_id(ip_address)
            integer_id = bin_id2int_id(binary_id)
            hex_id = int_id2hex_id(integer_id)
            data = {'ip_address': ip_address, 'network_address': network_address,
                    'host_ip_range': host_ip_range, 'broadcast_address': broadcast_address,
                    'number_of_host': number_of_host, 'number_of_usable_host': number_of_usable_host,
                    'subnet_mask': subnet_mask, 'wildcard_mask': wildcard_mask,
                    'binary_subnet_mask': binary_subnet_mask, 'ip_class': ip_class,
                    'cidr_notation': cidr_notation, 'ip_type': ip_type,
                    'short': short, 'binary_id': binary_id,
                    'integer_id': integer_id, 'hex_id': hex_id,
                    }
            form = CalculatorForm(create_subnet('Any'),initial={'ip_address':ip_address})    
            return render(request, 'calculator.html', {'form': form, 'data': data})
        return render(request, 'calculator.html', {'form': form})
    form = CalculatorForm(create_subnet('Any'))
    return render(request, 'calculator.html', {'form': form})
