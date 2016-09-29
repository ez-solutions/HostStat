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
    """
    test_hosts = [
        ['0', '4', '1'],
        ['1', '3', '0']
    ]
    results = stats.create_host_report(test_hosts)
    expected_host_id = '1'
    assert expected_host_id in results.keys(), "{} is expected to be found in the results".format(expected_host_id)
    print results

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

