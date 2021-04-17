import hcl
import os
from graphviz import Graph
import Resources
from pathlib import Path

def SGParser(rule):
    if type(rule) == type([]):
        lines = []
        for r in rule:
            lines.append(f'{r["from_port"]}\t{r["to_port"]}\t{r["protocol"]}\t{r["cidr_blocks"]}')
        return '\n'.join(lines)
    else:
        return f'{rule["from_port"]}\t{rule["to_port"]}\t{rule["protocol"]}\t{rule["cidr_blocks"]}'


def ACLParser(rule):
    if type(rule) == type([]):
        lines = []
        for r in rule:
            lines.append(f'{r["protocol"]}\t{r["rule_no"]}\t{r["action"]}\t{r["cidr_block"]}\t{r["from_port"]}\t{r["to_port"]}')
        return '\n'.join(lines)
    else:
        return f'{rule["protocol"]}\t{rule["rule_no"]}\t{rule["action"]}\t{rule["cidr_block"]}\t{rule["from_port"]}\t{rule["to_port"]}'

def logger(accessControl, fp):
    if accessControl.type in 'NACL':
        fp.write("NACL: " + NACL.name+'\n')
        fp.write("protocol\trule_no\taction\tcidr_blocks\tfrom_port\tto_port\n")
        localrules = NACL.getRules()
        fp.write("Ingress\n")
        fp.write(ACLParser(localrules[0]) + '\n')
        fp.write("Egress\n")
        fp.write(ACLParser(localrules[1]) + '\n')
        fp.write('\n')
    elif accessControl.type in 'Security Group':
        localrules = SG.getRules()
        fp.write("Security Group: " + SG.name +'\n')
        fp.write("from\tto\tproto\tcidr\n")
        fp.write("Ingress\n")
        fp.write(SGParser(localrules[0])+'\n')
        fp.write("Egress\n")
        fp.write(SGParser(localrules[1])+'\n')
        fp.write('\n')
    elif accessControl.type in 'EC2':
        localrules = accessControl.provisioner.inline
        fp.write("EC2 Provisioner: " + accessControl.name + '\n')
        for line in localrules:
            fp.write(line+'\n')
        fp.write('\n')
    else:
        print(accessControl.type +' ' + accessControl.name +" cannot be logged")


# TERRAFORM_DIR = r"terraform-aws-examples-master/03-instance-with-multiple-network"
# TERRAFORM_DIR = r'terraform-aws-examples-master/04-instance-with-loadbalancer'
# TERRAFORM_DIR = r'terraform-aws-examples-master/two-tier'
# TERRAFORM_DIR = r'terraform-aws-examples-master/05-autoscaling-group'
TERRAFORM_DIR = r'CloudFInal/'

terraformFolder = Path(TERRAFORM_DIR)
terraform_files = []
resourceList = []
resources = []

for a,b,files in os.walk(terraformFolder):
    for file in files:
        if file.endswith(".tf"):
            terraform_files.append(terraformFolder / file)

# print(terraform_files)

for file in terraform_files:
    with open(file, 'r') as f:
        obj =  hcl.load(f)

    for key, val in obj.items():
        if 'resource' in key:
            print(val)
            for k, v in val.items():
              resourceList.append((k,v))


for item in resourceList:
    print(item)
    # print(len(item[1]))
    if 'aws_vpc' in item[0]:
        # print(list(item[1].keys())[0])
        name = list(item[1].keys())[0]
        vpc = Resources.VPC(name, item[1][name]['cidr_block'])
        resources.append(vpc)

    if 'aws_instance' in item[0]:
        for instance in item[1].keys():
            name = instance
            # resources.append(Resources.ec2(name, item[1][name]['ami'], item[1][name]['instance_type'], item[1][name]['vpc_security_group_ids'], item[1][name]['subnet_id']))
            resources.append(Resources.ec2(name, item[1][name]))
            print(resources[-1].get())


    if 'aws_subnet' in item[0]:
        for subnet in item[1].keys():
            name = subnet
            # resources.append(Resources.subnet(name, item[1][name]['vpc_id'],item[1][name]['cidr_block']))
            resources.append(Resources.subnet(name, item[1][name]))


            for routeitem in resourceList:
                if 'association' in routeitem[0]:

                    for rte in routeitem[1].keys():
                        if name in routeitem[1][rte]['subnet_id']:
                            resources[-1].associateRoute(routeitem[1][rte]['route_table_id'].split('.')[1])

    if 'aws_network_acl' in item[0]:
        for acl in item[1].keys():
            resources.append(Resources.NACL(acl, item[1][acl]))

    if 'aws_security_group' in item[0]:
        for sg in item[1].keys():
            resources.append((Resources.SG(sg, item[1][sg])))

    if 'aws_route_table' in item[0] and 'association' not in item[0]:
        for route in item[1].keys():
            resources.append(Resources.RouteTable(route, item[1][route]))
    elif 'aws_route' in item[0] and 'association' not in item[0]:
        for route in item[1].keys():
            resources.append(Resources.Route(route, item[1][route]))

    if 'aws_internet_gateway' in item[0]:
        for igw in item[1].keys():
            resources.append(Resources.IGW(igw, item[1][igw]))


VPCs = [x for x in resources if x.getType() == 'VPC']
Subnets = [x for x in resources if x.getType() == 'Subnet']
EC2_instance = [x for x in resources if x.getType() == 'EC2']
NACLs =  [x for x in resources if x.getType() == 'NACL']
SGs =  [x for x in resources if x.getType() == 'Security Group']
RoutesTables =  [x for x in resources if x.getType() == 'RouteTable']
Routes =  [x for x in resources if x.getType() == 'Route']
IGWs =  [x for x in resources if x.getType() == 'IGW']

g = Graph("G", engine='fdp')



with open('accesscontrol.txt', 'w') as fp:
    with g.subgraph(name='clusterVPC') as v:
        for igw in IGWs:
            # g.edge('clusterVPC', "IGW\n" + igw.name)
            v.node("IGW\n" + igw.name)
        for NACL in NACLs:
            for net in NACL.subnet:
                v.edge("clusterSUBNET "+net.split('.')[1], f"NACL\n{NACL.name}")
            logger(NACL, fp)

        for route in RoutesTables:
            v.edge("ROUTE\n" + route.name, "IGW\n" + route.route['gateway_id'].split('.')[1])
        else:
            for route in Routes:
                v.edge("ROUTE\n" + route.name, "IGW\n" + route.gateway.split('.')[1])
        for SG in SGs:
            v.node('SG\n' + SG.name)
            logger(SG, fp)
        v.attr(label=f'VPC {VPCs[0].name}')

        for net in Subnets:

            if net.route:
                g.edge("clusterSUBNET "+net.name, f"ROUTE\n{net.route}")

            # v.edge("VPC\n"+VPC.name, "SUBNET\n"+net.name)
            # v.edge("SUBNET\n"+net.name, "ROUTE\n"+net.route)
            with v.subgraph(name='clusterSUBNET ' + net.name) as s:
                s.attr(label=f'Subnet {net.name}')
                for EC2 in EC2_instance:
                    # with v.subgraph(name='clusterSUBNET '+net.name) as s:
                    #     s.attr(label=f'Subnet {net.name}')
                        if net.name in EC2.subnet:
                            s.node("EC2 Instance\n"+EC2.name)
                            if EC2.provisioner:
                                logger(EC2, fp)
                            for SG in SGs:
                                # print(SG.name)
                                if SG.name in ' '.join(EC2.security_groups):
                                    v.edge("EC2 Instance\n" + EC2.name, "SG\n"+SG.name)
                                    

g.view()
