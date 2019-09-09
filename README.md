Consistent Hashing Load Balancer
===============================

This is an implementation of load balancing algorithm across distributed servers.
Each server receives the full set of objects [0,1,.., 4025] and the full set
of server ids [1, 2, .., 100]. This program takes the list of jobs and servers
from stdin and outputs the job distribution across servers.

Theory of Operation
-------------------

The algorithm uses consistent hashing. The top level data structure is a hash ring
that maintains a list of hashes representing the servers that are added in the 
system. For each server added, 3 hashes are created. This is done so that the
jobs will get distributed more evenly across the servers. If we have hashes 
spread more evenly across the namespace the better. These hashes are maintained 
in a sorted list. For example, if there are 10 servers, there are 30 hashes in 
the namespace of 0-4095 and they are arranged in ascending order in the hash ring. 
If there is collision while adding the hash in the list, an alternate hash that 
do not collide is created and added to the list.

When a job gets added to the system, it is hashed in the namespace of 0-4095. We 
go over the list of server hashes maintained in the hash ring until the hashed value
is less than the hash in the list. The server that produced that hash  will be the
owner of the job. If the input hash is higher than all the hashes in the list, the
job will be going to the server that produced the first hash in the list. Thus, even
though we have a list data structure, we are operating a cirular ring of hashes for
the lookup.

For example, if I have 3 servers with nodeId 0,1,2, I generate 6 hashes (3 each) and
sort them as shown below
nodeId  hash
1       1495
1       2640
0       2665
2       2947
0       2990
0       3539
1       3593
2       3923
2       4039

If a job with jobid 5 comes, and it hashes to 1861, the server hash that is next bigger
to 1861 is 2640 and it belongs to server nodeId 1. Hence, server Id 1 will be the owner 
of job 5. Jobid 3 produces hash 3121, it will go to server 0.

If server 1 goes down, nodeId 1 will be removed from the server hash list resulting in the
following order

0       2665
2       2947
0       2990
0       3539
2       3923
2       4039

Here, job id 5 will migrate from 1 to 0 since 2665 is the next big hash to 1861. Jobid 3 
will still go to server 0 since 3539 is still the next bigger hash than 3121. Thus only
the jobs that had server removed migrates and the allocation  of the rest of the jobs 
remain the same.

Similarly, when new jobs are added, the old jobs retain their server allocation. 

Steps to run the program
-----------------------

The program is interactive. It gets the list of jobs and servers from the user and outputs
the job distribution across the servers.

Run the cmd "python lb.py" as follows. It asks to give the list of jobs and servers.

Kannan_laptop$ ./lb.py

This is a program to do consistent hashing of jobs to servers provided.

Enter comma separated jobs list followed by enter at the prompt "Jobs" - e.g Jobs=>0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22

And comma separated server list followed by enter at the prompt "Servers" - e.g Servers=>0,1,2,3,4

The program will output the distribution of jobs to servers

Jobs=>0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22

Servers=>0,1,2,3,4

Node is 1 and job list is ['1', '6', '12', '13', '14', '15', '16']

Node is 0 and job list is ['0', '20']

Node is 3 and job list is ['3', '8', '9', '10', '11']

Node is 2 and job list is ['2', '21', '22']

Node is 4 and job list is ['4', '5', '7', '17', '18', '19']

Jobs=>0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22

Servers=>0,1,3,4

Node is 1 and job list is ['1', '6', '12', '13', '14', '15', '16']

Node is 0 and job list is ['0', '2', '20']

Node is 3 and job list is ['3', '8', '9', '10', '11']

Node is 4 and job list is ['4', '5', '7', '17', '18', '19', '21', '22']


As you can see above, the jobs are not moved around from existing servers
when I removed server 2 from the list


Test Cases and Sample outputs
----------------------------

To run test cases run "python tests.py"
There are test cases that remove/add servers and adds jobs and check the resulting
job distributions. I have added an utility "getNoJobsMoved()" in utilities.py. I 
call this method from my unittest to get the list of servers that have the old jobs
not removed. Then I check whether the number of servers that have no previous jobs
migrated is within expected limit.  Also the output of the test run is in a file 
called "test_output" for manual verification and it has an entry called "NoJobsMovedNodes" 
that has the list of servers with no previous jobs removed from its list.

The current test cases are

Test case-1
-----------
Add 20 server ids and check whether  60 hashes populated in the ring


Test case-2
-----------
Provide more servers than jobs and check whether the jobs are allocated. 
Check the "test_output" file

Test case-3
----------
Create allocation for  22 jobs among 5 servers
Check the "test_output" file

Test case-4
----------
Remove one server and check there is no job movement from existing servers
Check the "test_output" file. You will find an entry as below showing no job movement for 
all 4 existing servers

NoJobsMovedNodes:
["1", "0", "3", "4"]


Test case-5
----------
Add 3 more jobs and check there is no job movement from existing servers
Check the "test_output" file. You will find an entry as below showing no job movement for 
all 4 existing servers

NoJobsMovedNodes:
["1", "0", "3", "4"]

Test case-6
----------
Add a server and check the job movement from existing servers
Check the "test_output" file. You will find an entry as below showing very 
minimal job movement when you added a server. 3 out of 4 servers did not 
see any job movement 

NoJobsMovedNodes:
["1", "0", "3"]

