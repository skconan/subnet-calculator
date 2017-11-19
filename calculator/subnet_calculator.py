def create_subnet(network_class):
    subnet_class = {}
    subnet_tuple = ()
    subnet = 11111111111111111111111111111111
    subnet_str = str(subnet)
    subnet_str = (str(int(subnet_str[0:8], 2)) + '.'
                  + str(int(subnet_str[8:16], 2)) + '.'
                  + str(int(subnet_str[16:24], 2)) + '.'
                  + str(int(subnet_str[24:32], 2)) + ' /32')
    subnet_tuple += ((subnet_str, subnet_str),)

    for i in range(0, 31):
        subnet -= pow(10, i)
        subnet_str = str(subnet)
        subnet_str = (str(int(subnet_str[0:8], 2)) + '.'
                      + str(int(subnet_str[8:16], 2)) + '.'
                      + str(int(subnet_str[16:24], 2)) + '.'
                      + str(int(subnet_str[24:32], 2)) + ' /'
                      + str(31 - i))
        subnet_tuple += ((subnet_str, subnet_str),)
        if 31 - i == 24:
            subnet_class['C'] = subnet_tuple
        elif 31 - i == 16:
            subnet_class['B'] = subnet_tuple
        elif 31 - i == 8:
            subnet_class['A'] = subnet_tuple
        elif 31 - i == 1:
            subnet_class['Any'] = subnet_tuple

    return subnet_class[network_class]


def ip_class_is(ip_address):
    ip = int(ip_address.split('.')[0])
    if 0 <= ip <= 127:
        return 'A'
    elif 128 <= ip <= 191:
        return 'B'
    elif 192 <= ip <= 223:
        return 'C'
    elif 224 <= ip <= 239:
        return 'D'
    else:
        return 'E'


def subnet2wildcard(subnet_mask):
    wildcard_mask = ''
    for subnet in subnet_mask.split('.'):
        wildcard_mask += str(255 - int(subnet)) + '.'
    return wildcard_mask[0:-1]


def bin_subnet(subnet_mask):
    binary_subnet_mask = ''
    for subnet in subnet_mask.split('.'):
        binary_subnet_mask += "{0:08b}".format(int(subnet)) + '.'
    return binary_subnet_mask[0:-1]


def ip2bin_id(ip_address):
    binary_id = ''
    for ip in ip_address.split('.'):
        binary_id += "{0:08b}".format(int(ip))
    return binary_id


def bin_id2int_id(binary_id):
    integer_id = int(binary_id, 2)
    return integer_id


def int_id2hex_id(integer_id):
    hex_id = hex(integer_id)
    return hex_id

def masking(ip_address,subnet_mask):
    result = ''
    for (ip,subnet) in zip(ip_address.split('.'),subnet_mask.split('.')):
        result += str(int(ip)&int(subnet))+'.'
    return result[0:-1]

def number_of_host_is(cidr_notation):
    return pow(2,32-int(cidr_notation))

def broadcast_address_is(ip_address,wildcard_mask):
    result = ''
    for (ip,subnet) in zip(ip_address.split('.'),wildcard_mask.split('.')):
        result += str(int(ip)|int(subnet))+'.'
    return result[0:-1]

def host_ip_range_is(network_address,broadcast_address):
    ip_min = network_address.split('.')
    ip_max = broadcast_address.split('.')
    ip_min[3] = str(int(ip_min[3]) + 1)
    ip_max[3] = str(int(ip_max[3]) - 1)
    if ip_min[3] == ip_max[3] or ip_min[3] == '256' or ip_max[3] == '-1':
        return None 
    print(ip_min)
    print(ip_max)
    return ip_min[0]+'.'+ip_min[1]+'.'+ip_min[2]+'.'+ip_min[3]+' - '+ip_max[0]+'.'+ip_max[1]+'.'+ip_max[2]+'.'+ip_max[3]

def ip_type_is(ip_address):
    ip = ip_address.split('.')
    if int(ip[0]) == 10:
        return 'Private'
    if int(ip[0]) == 172 and 16 <= int(ip[1]) <= 31:
        return 'Private'
    if int(ip[0]) == 192 and int(ip[1]) == 168:
        return 'Private'
    return 'Public'
