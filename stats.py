# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Assumptions:
1. Input files are in the same directory as the source file
2. Input file names are: HostState.txt, InstanceState.txt
3. Only integers separated by comma are allowed in input files
4. Any number after the 3rd nubmer in a row will be ignored.
5. Empty lines and spaces are ignored.
6. Host id in InstanceState.txn must exist in HostState.txt.
7. host_id in HostState.txt MUSTN'T appeare multiple times




Customer


"""

import sys
from bson.json_util import dumps


# CONSTANTS
HOSTID = 0
INSTANCEID = 0
CUSTOMERID = 1
SLOTS = 1
DATACENTER = 2

def read_file(filename):
    """
    Read a given file in the current directory
    """
    with open(filename) as f:
        # Read file content and remove spaces and EOL
        try:
            # file =  [l for l in f if l]
            # print file
            data = [
                [x.replace('\r\n', '') for x in line.split(",") if x.replace('\r\n', '').strip()]
                for line in f if line.replace('\r\n', '')
            ]
        except:
            raise Exception('Invalid file format: ' + filename)
        # Validate data type
        try:
            for line in data:
                int(''.join(line))
        except ValueError:
            raise Exception('Invalid data found in file: ' + filename)
    return data

hosts = read_file('HostState.txt')
instances = read_file('InstanceState.txt')

print "INSTANCES: {}".format(instances)
print "HOSTS: {}".format(hosts)

host_report = {}
for host in hosts:
    host_id = host[0]
    if not host_id in host_report.keys():
        host_report.update({
            host_id: {
                'slots': host[1],
                'instances': [],
                'datacentre': host[2]
            }
        })
    else:
        raise Exception('Duplicate host_id found!!!')

customer_report = {}
# customer_ids = get_customer_ids(instances)
for instance in instances:
    customer_id = instance[1]
    host_id = instance[-1]
    instance_id = instance[0]
    
    # Update host report
    if not instance_id in host_report[host_id]['instances']:
        host_report[host_id]['instances'].append(instance_id)

    if not customer_id in customer_report.keys():
        customer_report.update({
            customer_id: {
                'instance_ids': [],
                'hosts': {}, # {host_id: [list of instance on this host]}
                'datacentres': {} # {datacentre_id: [list of instances on this datacentre]}
            }
        })
    # Update instances
    print dumps(customer_report, indent=4)
    print 
    if not instance_id in customer_report[customer_id]['instance_ids']:
        customer_report[customer_id]['instance_ids'].append(instance_id)
    # Update hosts
    if not host_id in customer_report[customer_id]['hosts'].keys():
        customer_report[customer_id]['hosts'].update({
            host_id: []
        })
        customer_report[customer_id]['hosts'][host_id].append(instance_id)
    else:
        if not instance_id in customer_report[customer_id]['hosts'][host_id]:
            customer_report[customer_id]['hosts'][host_id].append(instance_id)
    
    # Update datacentre
    datacentre_id = host_report[host_id]['datacentre']
    if not datacentre_id in customer_report[customer_id]['datacentres'].keys():
        customer_report[customer_id]['datacentres'].update({
            datacentre_id: []
        })

    if not instance_id in customer_report[customer_id]['datacentres'][datacentre_id]:
        customer_report[customer_id]['datacentres'][datacentre_id].append(instance_id)


# Calculate the customer with the largest instance fraction on a single host
max_fraction_host = [0.0]
max_fraction_dc = [0.0]
max_customer_host = [-1]
max_customer_dc = [-1]
print dumps(customer_report, indent=4)

for customer_id, customer in customer_report.iteritems():
    # print customer_id
    # print customer
    total_instances = len(customer['instance_ids'])
    # print 'Total Instances: {}'.format(total_instances)
    # print 'Total hosts: {}'.format(len(customer['hosts']))
    # Customer has largest fractioin of instance on a host
    for host_id, instances_on_host in customer['hosts'].iteritems():
        # print customer['hosts']
        # print host_id
        # print instances_on_host
        fraction_host = float(len(instances_on_host)) / float(total_instances)
        # print "host fraction on host: {} is {}".format(host_id, fraction_host)
        if fraction_host > max_fraction_host[-1]:
            max_fraction_host = [fraction_host]
            max_customer_host = [customer_id]
        elif fraction_host == max_fraction_host[-1]:
            max_fraction_host.append(fraction_host)
            max_customer_host.append(customer_id)
    # Customer has largest fraction
    for dc_id, instances_on_dc in customer['datacentres'].iteritems():
        fraction_dc = float(len(instances_on_dc)) / float(total_instances)
        print fraction_dc
        if fraction_dc > max_fraction_dc[-1]:
            max_fraction_dc = [fraction_dc]
            max_customer_dc = [customer_id]
        elif fraction_dc == max_fraction_dc[-1]:
            max_fraction_dc.append(fraction_dc)
            max_customer_dc.append(customer_id)

# print max_customer_host
print "max_customer_host: {} on {}".format(max_fraction_host, max_customer_host)

# print max_customer_dc
print "max_customer_dc: {} on {}".format(max_fraction_dc, max_customer_dc)



# print dumps(host_report, indent=4)

available_hosts = []
for host_id, status in host_report.iteritems():
    if int(status['slots']) - len(status['instances']) >= 1:
        available_hosts.append(host_id)

print available_hosts





