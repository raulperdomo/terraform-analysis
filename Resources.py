class Resources():
    def __init__(self, name):
        self.name = name
    def get(self):
        return self.name
    def getType(self):
        return None

class Provisioner(Resources):
    def __init__(self, creationDict):
        if 'remote-exec' in creationDict.keys():
            self.inline = creationDict['remote-exec']['inline']

class VPC(Resources):
    def __init__(self, name, cidr):
        self.name = name
        self.cidr = cidr
        self.type = 'VPC'

    def getType(self):
        return self.type

    def get(self):
        return f"VPC Name: {self.name} \nCIDR Block: {self.cidr}"

class ec2(Resources):

    def __init__(self, name, creationDict):
        self.name = name
        self.type = 'EC2'
        self.instance_type = None
        self.ami = None
        self.security_groups = None
        self.subnet = None
        self.provisioner = None
        for k,v in creationDict.items():
            print(k,v)
            if 'ami' in k:
                self.ami = v
            elif 'instance_type' in k:
                self.instance_type = v
            elif 'security_group' in k:
                self.security_groups = v
            elif 'subnet_id' in k:
                self.subnet = v
            elif 'provisioner' in k:
                self.provisioner = Provisioner(v)
        print(f"{self.getType()} {self.name} created.\n")

    def get(self):
         return f"Instance Name: {self.name}\nAmi: {self.ami}\nInstance Type: {self.type}\nSGs: {str(self.security_groups)}\nSubnet: {self.subnet}"

    def getType(self):
        return self.type

class subnet(Resources):
    def __init__(self, name, creationDict):
        print(creationDict.keys())
        self.name = name
        self.vpc_id = None
        self.cidr = None
        self.type = 'Subnet'
        self.tags = None
        self.route = None
        for k,v in creationDict.items():
            print(k,v)
            if 'vpc_id' in k:
                self.vpc_id = v
            if 'cidr_block' in k:
                self.cidr = v
            if 'tags' in k:
                self.tags = v
        print(f"{self.getType()} {self.name} created.\n")

    def getType(self):
        return self.type

    def get(self):
        return f'Subnet Name: {self.name}\nVPC ID: {self.vpc_id}\nCIDR Block: {self.cidr}'

    def associateRoute(self, route):
        self.route = route

class NACL(Resources):
    def __init__(self, name, creationDict):
        self.name = name
        self.vpc = None
        self.subnet = None
        self.ingress = None
        self.egress = None
        self.tags = None
        self.type = "NACL"
        for k,v in creationDict.items():
            print(k,v)
            if 'vpc_id' in k:
                self.vpc_id = v
            if 'subnet_ids' in k:
                self.subnet = v
            if 'ingress' in k:
                self.ingress = v
            if 'egress' in k:
                self.egress = v
            if 'tags' in k:
                self.tags = v
        print(f"{self.getType()} {self.name} created.\n")

    def getType(self):
        return self.type

    def getRules(self):
        return self.ingress, self.egress

    def get(self):
        return f'NACL Name: {self.name}\nAssociated Subnet: {self.subnet}\nIngress Rules: {self.ingress}\nEgress Rules: {self.egress}'

class RouteTable(Resources):
    def __init__(self, name, creationDict):
        self.name = name
        self.vpc = None
        self.route = None
        self.tags = None
        self.type = "RouteTable"
        for k,v in creationDict.items():
            print(k,v)
            if 'vpc_id' in k:
                self.vpc_id = v
            if 'route' in k:
                self.route = v
            if 'tags' in k:
                self.tags = v
        print(f"{self.getType()} {self.name} created.\n")

    def getType(self):
        return self.type

class Route(Resources):
    def __init__(self, name, creationDict):
        self.name = name
        self.route_table_id = None
        self.destination_cidr_block = None
        self.gateway = None
        self.tags = None
        self.type = "Route"
        for k,v in creationDict.items():
            print(k,v)
            if 'route_table_id' in k:
                self.vpc_id = v
            if 'destination_cidr_block' in k:
                self.route = v
            if 'gateway_id' in k:
                self.gateway = v
            if 'tags' in k:
                self.tags = v
        print(f"{self.getType()} {self.name} created.\n")

    def getType(self):
        return self.type

class SG(Resources):
    def __init__(self, name, creationDict):
        self.name = name
        self.ingress = None
        self.egress = None
        self.type = "Security Group"
        for k,v in creationDict.items():
            print(k,v)
            if 'ingress' in k:
                self.ingress = v
            if 'egress' in k:
                self.egress = v

        print(f"{self.getType()} {self.name} created.\n")

    def getType(self):
        return self.type

    def getRules(self):
        return self.ingress, self.egress

class IGW(Resources):
    def __init__(self, name, creationDict):
        self.name = name
        self.vpc_id = None
        self.tags = None
        self.type = "IGW"
        for k,v in creationDict.items():
            print(k,v)
            if 'vpc_id' in k:
                self.ingress = v
            if 'tags' in k:
                self.egress = v

        print(f"{self.getType()} {self.name} created.\n")

    def getType(self):
        return self.type