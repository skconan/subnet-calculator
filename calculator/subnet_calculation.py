class CreateData():
    def __init__(self):
        self.subnet_mask = self.create_subnet()

    def subnet_bin2dec(self, subnet, cidr_notation):
        subnet_str = str(subnet)
        result = ''
        for i in range(0, 25, 8):
            if i is not 0:
                result += '.'
            result += str(int(subnet_str[i:i + 8], 2))
        result += ' /' + str(cidr_notation)
        return result

    def create_subnet(self):
        subnet_mask = {}
        subnet_mask['default'] = (
            ('default', 'Select a network class before subnet'),)
        subnet_tuple = ()
        subnet = 11111111111111111111111111111111
        subnet_str = self.subnet_bin2dec(subnet, 32)
        subnet_tuple += ((subnet_str, subnet_str),)

        for i in range(0, 31):
            subnet -= pow(10, i)
            subnet_str = self.subnet_bin2dec(subnet, 31 - i)
            subnet_tuple += ((subnet_str, subnet_str),)
            if 31 - i == 24:
                subnet_mask['C'] = subnet_tuple
            elif 31 - i == 16:
                subnet_mask['B'] = subnet_tuple
            elif 31 - i == 8:
                subnet_mask['A'] = subnet_tuple
            elif 31 - i == 1:
                subnet_mask['Any'] = subnet_tuple
        return subnet_mask

    def get_subnet(self, network_class):
        return self.subnet_mask[network_class]


class SubnetCalculation():
    def __init__(self, network_class, subnet_mask, ip_address):
        self.network_class = network_class
        self.network_address_bin = None
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask.split('/')[0]
        self.wildcard_mask = self.get_wildcard_mask()
        self.network_address = self.get_network_address()
        self.broadcast_address = self.get_broadcast_address()
        self.cidr_notation = subnet_mask.split('/')[1]
        self.short = self.ip_address + ' /' + self.cidr_notation
        self.bin_id = self.get_bin_id()
        self.int_id = self.get_integer_id()
        self.no_host = self.get_total_number_of_host()

    def calculate(self):
        data = {}
        data['ip_address'] = self.ip_address
        data['network_address'] = self.network_address
        data['host_ip_range'] = self.get_host_ip_range()
        data['broadcast_address'] = self.broadcast_address
        data['number_of_host'] = self.no_host
        data['number_of_usable_host'] = max(self.no_host - 2, 0)
        data['subnet_mask'] = self.subnet_mask
        data['wildcard_mask'] = self.wildcard_mask
        data['binary_subnet_mask'] = self.get_subnet_mask_bin()
        data['ip_class'] = self.get_ip_class()
        data['cidr_notation'] = '/' + self.cidr_notation
        data['ip_type'] = self.get_ip_type()
        data['short'] = self.short
        data['binary_id'] = self.bin_id
        data['integer_id'] = self.int_id
        data['hex_id'] = self.get_hex_id()
        return data

    def get_subnet_mask_bin(self):
        subnet_bin = ''
        for ip in self.subnet_mask.split('.'):
            subnet_bin += "{0:08b}".format(int(ip)) + '.'
        return subnet_bin[0:-1]

    def get_network_address(self):
        result = ''
        for (ip, subnet) in zip(self.ip_address.split('.'), self.subnet_mask.split('.')):
            result += str(int(ip) & int(subnet)) + '.'
        return result[0:-1]

    def get_wildcard_mask(self):
        wildcard_mask = ''
        for subnet in self.subnet_mask.split('.'):
            wildcard_mask += str(255 - int(subnet)) + '.'
        return wildcard_mask[0:-1]

    def get_ip_class(self):
        ip = int(self.ip_address.split('.')[0])
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

    def get_ip_type(self):
        ip = self.ip_address.split('.')
        if ((int(ip[0]) == 172 and 16 <= int(ip[1]) <= 31)
            or (int(ip[0]) == 192 and int(ip[1]) == 168)
                or int(ip[0]) == 10):
            return 'Private'
        return 'Public'

    def get_bin_id(self):
        bin_id = ''
        for ip in self.ip_address.split('.'):
            bin_id += "{0:08b}".format(int(ip))
        return bin_id

    def get_integer_id(self):
        return int(self.bin_id, 2)

    def get_hex_id(self):
        return hex(self.int_id)

    def get_total_number_of_host(self):
        return pow(2, 32 - int(self.cidr_notation))

    def get_broadcast_address(self):
        result = ''
        for (ip, subnet) in zip(self.ip_address.split('.'), self.wildcard_mask.split('.')):
            result += str(int(ip) | int(subnet)) + '.'
        return result[0:-1]

    def get_host_ip_range(self):
        ip_min = self.network_address.split('.')
        ip_max = self.broadcast_address.split('.')
        ip_min[3] = str(int(ip_min[3]) + 1)
        ip_max[3] = str(int(ip_max[3]) - 1)
        if self.no_host <= 2:
            return None
        return ip_min[0] + '.' + ip_min[1] + '.' + ip_min[2] + '.' + ip_min[3] + ' - ' + ip_max[0] + '.' + ip_max[1] + '.' + ip_max[2] + '.' + ip_max[3]
