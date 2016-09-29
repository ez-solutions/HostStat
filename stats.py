# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
from bson.json_util import dumps

def read_file(filename):
    """
    Read a given file in the current directory
    """
    print "Reading {} ...".format(filename)
    with open(filename) as f:
        # Read file content and remove spaces and EOL
        try:
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

def create_host_report(hosts):
    """
    """
    print "Creating a host report ..."
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
    return host_report

def create_customer_report(host_report, instances):
    """
    """
    print "Create a customer report ..."
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
    return customer_report

def get_largest_fraction(customer_report):
    """
    """
    print "Calculating fractions ..."
    # Calculate the customer with the largest instance fraction on a single host
    max_fraction_host = [0.0]
    max_fraction_dc = [0.0]
    max_customer_host = [-1]
    max_customer_dc = [-1]

    for customer_id, customer in customer_report.iteritems():
        total_instances = len(customer['instance_ids'])
        # Customer has largest fractioin of instance on a host
        for host_id, instances_on_host in customer['hosts'].iteritems():
            fraction_host = float(len(instances_on_host)) / float(total_instances)
            if fraction_host > max_fraction_host[-1]:
                max_fraction_host = [fraction_host]
                max_customer_host = [customer_id]
            elif fraction_host == max_fraction_host[-1]:
                max_fraction_host.append(fraction_host)
                max_customer_host.append(customer_id)
        # Customer has largest fraction
        for dc_id, instances_on_dc in customer['datacentres'].iteritems():
            fraction_dc = float(len(instances_on_dc)) / float(total_instances)
            if fraction_dc > max_fraction_dc[-1]:
                max_fraction_dc = [fraction_dc]
                max_customer_dc = [customer_id]
            elif fraction_dc == max_fraction_dc[-1]:
                max_fraction_dc.append(fraction_dc)
                max_customer_dc.append(customer_id)

    largest_fractioin_host = {}
    for i in xrange(len(max_customer_host)):
        largest_fractioin_host.update({
            max_customer_host[i]: max_fraction_host[i]
        })
    
    largest_fractioin_dc = {}
    for i in xrange(len(max_customer_dc)):
        largest_fractioin_dc.update({
            max_customer_dc[i]: max_fraction_dc[i]
        })
    return largest_fractioin_host, largest_fractioin_dc    

def get_available_hosts(host_report):
    """
    """
    print "Finding hosts with available slots ..."
    available_hosts = []
    for host_id, status in host_report.iteritems():
        if int(status['slots']) - len(status['instances']) >= 1:
            available_hosts.append(host_id)
    available_hosts.sort(key=int)
    return available_hosts

def write_stats_file(max_fraction_host, max_fraction_dc, available_hosts):
    """
    filename = Statistics.txt
    --------------------------------------------------------------------------------------------------------------------
    |   HostClustering:<customerID>,<fractionOfFleetOnHost>                                                            |
    |   DatacentreClustering:<customerID>,<fractionOfFleetInDataCentre>                                                |
    |   AvailableHosts:<hostID_1>,<hostID_2>,...                                                                       |
    --------------------------------------------------------------------------------------------------------------------
    """
    print "Writing output file: {}".format("Statistics.txt")
    f = open('Statistics.txt', 'w')
    f.write('HostClustering:')
    for customer_id, fraction in max_fraction_host.iteritems():
        f.write('{},{}'.format(customer_id, fraction))
    f.write('\n')
    f.write('DatacentreClustering:')
    for customer_id, fraction in max_fraction_dc:
        f.write('{},{}'.format(customer_id, fraction))
    f.write('\n')
    f.write('AvailableHosts:')
    for i in xrange(len(available_hosts)):
        f.write('{}'.format(available_hosts[i]))
        if i != (len(available_hosts)-1):
            f.write(',')
    f.close()

if __name__ == '__main__':

    hosts_file = 'HostState.txt'
    instances_file = 'InstanceState.txt'
    
    hosts = read_file(hosts_file)
    instances = read_file(instances_file)

    host_report = create_host_report(hosts)
    customer_report = create_customer_report(host_report, instances)
    largest_fraction_host, largest_fraction_dc = get_largest_fraction(customer_report)
    available_hosts = get_available_hosts(host_report)
    write_stats_file(largest_fraction_host, largest_fraction_dc, available_hosts)
    print "Done"
    print "Please refer to the results in Statistics.txt "