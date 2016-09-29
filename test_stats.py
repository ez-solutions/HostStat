# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import imp
from bson.json_util import dumps

import stats 

def test_read_file(file_name):
    """
    """
    expected_results = [
        ['2','4','0'],
        ['5','4','0'],
        ['7','3','0']
    ]
    results = stats.read_file(file_name)
    for result in expected_results:
        assert result in results, '{} was NOT found after reading {}\n'.format(result, file_name) 


def test_create_host_report():
    """
    Test create_host_report() by giving a expected input
    """
    test_hosts = [
        ['0', '4', '1'],
        ['1', '3', '0']
    ]
    results = stats.create_host_report(test_hosts)
    expected_host_id = '1'
    assert expected_host_id in results.keys(), "{} is expected to be found in the results".format(expected_host_id)
    expected_keys = ['slots', 'instances', 'datacentre']
    for key in expected_keys:
        assert key in results[expected_host_id].keys(),  \
            '{} is expected to be in host report, but not found in: {}.'.format(key, results[expected_host_id].keys())

def test_create_customer_report():
    """
    Test create_customer_report() function by giving a expected input
    """
    instances = [
        ['1', '2', '0'],
        ['2', '1', '1'],
    ]
    host_report = {
        '0': {
            'slots': 3,
            'instances': [],
            'datacentre': '1'
        },
        '1': {
            'slots': 2,
            'instances': [],
            'datacentre': '0'
        }
    }
    results = stats.create_customer_report(host_report, instances)
    
    expected_host_report = {
        "1": {
            "instances": [
                "2"
            ], 
            "slots": 2, 
            "datacentre": "0"
        }, 
        "0": {
            "instances": [
                "1"
            ], 
            "slots": 3, 
            "datacentre": "1"
        }
    }

    expected_customer_report = {
        "1": {
            "datacentres": {
                "0": [
                    "2"
                ]
            }, 
            "hosts": {
                "1": [
                    "2"
                ]
            }, 
            "instance_ids": [
                "2"
            ]
        }, 
        "2": {
            "datacentres": {
                "1": [
                    "1"
                ]
            }, 
            "hosts": {
                "0": [
                    "1"
                ]
            }, 
            "instance_ids": [
                "1"
            ]
        }
    }
    assert cmp(results, expected_customer_report) == 0, "Expected: {}, but got: {}".format(expected_customer_report, results)
    assert cmp(host_report, expected_host_report) == 0, "Expected: {}, but got: {}".format(expected_host_report, host_report)

if __name__ == '__main__':

    hosts_file = sys.argv[1] 
    instances_file = sys.argv[2]

    try:
        print "\nStart testing: read_file()"
        test_read_file(hosts_file)
    except Exception as msg:
        print "FAILED: {}".format(msg)
    else:
        print "PASSED"

    try:
        print "\nStart testing: create_host_report()"
        test_create_host_report()
    except Exception as msg:
        print "FAILED: {}".format(msg)
    else:
        print "PASSED"

    try:
        print "\nStart testing: create_customer_report()"
        test_create_customer_report()
    except Exception as msg:
        print "FAILED: {}".format(msg)
    else:
        print "PASSED"