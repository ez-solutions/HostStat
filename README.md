Motivation
------------------------------------------------------------------------------------------------------------------------
Python is one of the mainstream Object Orientated languages and also the language I'm most comfortable with. Python is
also very flexible on string manipulation. For this specific prolem, a Python dictionary can be easily created to track
each customer's instances, host, and datacentre, which can be mapped to customer id without implementing any specific
searching algorithms.


Assumptions:
------------------------------------------------------------------------------------------------------------------------
1. Input files are in the same directory as the source file
2. Only integers separated by comma are allowed in input files
3. Any values after the 3rd nubmer in a row will be ignored.
4. Empty lines and spaces are ignored.
5. Host id in InstanceState.txn must exist in HostState.txt.
6. Duplicate host_id in HostState.txt is not allowed
7. Duplicate instance_id in InstancesState.txt in not allowed


Largest Fractions
------------------------------------------------------------------------------------------------------------------------
The fraction of a fleet of instances on a host of a customer is calculated as following:
    it's a ratio of a customer's intances on a single host and its total number of instances
If there are multiple customers with the same largest fractions, they all will be considered.

The fracation of a fleet of instances on a datacentre of a customer is calculated as following:
    it's a ratio of a customer's intances on a single datacentre and its total number of instances
If there are multiple customers with the same largest fractions, they all will be considered.


Available Hosts
------------------------------------------------------------------------------------------------------------------------
To find the available host, i.e. host with at least 1 slot available, all intances running on each host are reported,
then compare with total slots on the host.


Execution
------------------------------------------------------------------------------------------------------------------------
sh run.sh


Output
------------------------------------------------------------------------------------------------------------------------
A file named "Statistics.txt" will be create in the root directory for a successful exection.


Tests
------------------------------------------------------------------------------------------------------------------------
To run test: sh run_test.sh
Tests will cover the following basic functions:
    read_file()
    create_host_report()
    create_customer_report()


Future Work and Known Bugs
------------------------------------------------------------------------------------------------------------------------
If there are multiple customer with the same largest fractions, the customer and fraction paire must be separated by
commas.

For this code to work for a large size of hosts and instances files, a parallel library (mpi4py) can be used to read 
both files. Then hosts or instances data can be split into chunks, distributed and processed on multiple threads.