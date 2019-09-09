#!/usr/bin/python

import primes
import binascii
import traceback
import sys
import pdb


'''
@author: Kannan Narayanan

An implementation of load balancing algorithm across distributed servers. 
Each server receives the full set of objects [0,1,.., 4095] and the full set 
of server ids [0,1, .., 999]. This program takes the list of jobs and servers
from stdin and outputs the job distribution across servers.

The algorighm uses consistent hashing. The ring has a list of nodes that are 
hashed from the server id. If there is a collision in hashing an alternate 
hash is selected.  For each server, 3 hash entries are created so that the
jobs will get distributed in a better fashion across the servers. When job
is added the hash of the server closest to the job  hash  is selected
for that job.

This program when run, interactively gets the list of jobs, servers and outputs
the job distribution

'''

NUM_JOBS = 4095

class Node(object):

    '''
    A class that represents the node in our hash ring. For each server provided
    as input 3 of these objects are instantiated. For the first hash, the id
    input is used and for the next two, string to be appended is passed as argument
    '''
   
    def  __init__(self, id, append = None):
        self.id = id
        if append:
           appended_id = id + append
           self.hashId = (binascii.crc32(appended_id)% (1<<32))%NUM_JOBS
        else:
           self.hashId = (binascii.crc32(id)% (1<<32))%NUM_JOBS
        

class Ring(object):

    ''' 
    This class is the main hash ring class. It has a list of nodes. Methods
    are provided for adding a node(when server gets added), getting node (when
    job gets added. There is also a method to check whether there is a hash 
    collision when adding the node.
    '''

    def __init__(self):
        self.nodes = []
        
    def addNodeHelper(self, nodeId, append = None):

        '''
        See the description of addNode() function for more details. This is just 
        a helper function that gets called 3 times for each server node added.
        '''

        if append:
             node =  Node(nodeId, append)
        else: 
             node =  Node(nodeId)
        if self.checkHashExists(node.hashId):
            # Rehash here
            for i in range(len(primes.primes)):
                 if not self.checkHashExists(primes.primes[i] + node.hashId):   
                     node.hashId = primes.primes[i] + node.hashId
        self.nodes.append(node)

    def addNode(self, nodeId):

        '''
        When a server gets added, this method is called. It hashes the nodeId of 
        the server and checks whether hash already exists in the nodes list and
        then inserts the node. If hash already exists, the hash will be added to
        prime numbers that does not cause collision. The process is repeated 3 
        times for each server.  For the second and third time, a fixed string is
        appended to the server id to create the hash. 
        '''

        self.addNodeHelper(nodeId)
        self.addNodeHelper(nodeId, "2")
        self.addNodeHelper(nodeId, "15")
        self.nodes.sort(key=lambda x: x.hashId)


    def checkHashExists(self, val):
        for node in self.nodes:
           if val == node.hashId:
               return True
        return False


    def removeNode(self, Node):
        del self.nodes[node]


    def getNode(self, value):

        '''
        This method goes through the list sorted based on hash and finds 
        the entry that is just above the input input hash value. If it 
        reaches the end, return the 0th element 
        ''' 

        for entry in self.nodes:
            if entry.hashId < value:
                continue
            else:
               return entry.id 
        if entry == self.nodes[-1]:
            return self.nodes[0].id 


    def dumpNodes(self):
       print "Dumping nodes "  + str(len(self.nodes))
       for entry in self.nodes:
           print entry.id, entry.hashId
         

def loadBalance(newJobs, newServers, ring, distribution):

    '''
    This method populates the nodes in the ring with the input
    server ids and then hashes jobs to find the appropriate
    bucket in the hash ring. It creates the dictionary showing
    the distribution of jobs to servers.
    '''
    #Error checking
    if not ring or distribution is None:
        print ("Ring and distribution not present")
        return
    if len(newJobs)==0 or len(newServers) == 0:
        print ("Jobs or servers empty")
        return
    if len(newJobs) > 4096:
        print ("Jobs exceeded limit 4096")
        return
       
    if len(newServers) > 1000:
        print ("Servers exceeded limit 1000")
        return
    distribution.clear()
    del ring.nodes[:]
    for i in newServers:
        ring.addNode(i) 
    #ring.dumpNodes() 
    for  i  in newJobs:
        myHash = (binascii.crc32(i)% (1<<32))%NUM_JOBS
        #print myHash,i
        nodeId = ring.getNode(myHash)
        if nodeId in distribution:
           distribution[nodeId].append(i)
        else:
           distribution[nodeId] = [i]
    for key in distribution.keys():
        print ("Node is {} and job list is {}".format(key, distribution[key]))

def goInteractive():

    '''
    This method gets the list of jobs and servers from stdin and calls the 
    loadBalance() method
    '''

    ring = Ring()
    distribution = {}
    print("This is a program to do consistent hashing of jobs to servers provided.\n")
    print('Enter comma separated jobs list followed by enter at the prompt "Jobs" - e.g Jobs=>0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22')
    print('And comma separated server list followed by enter at the prompt "Servers" - e.g Servers=>0,1,2,3,4\n')
    print("The program will output the distribution of jobs to servers\n")
    while True:
       jobsInput =raw_input("Jobs=>")
       if jobsInput == '':
	   print("Empty input encountered. Try again")
           continue
       serversInput =raw_input("Servers=>")
       if serversInput == '':
	   print("Empty input encountered. Try again")
           continue
       
       newJobs = jobsInput.split(',')
       newServers = serversInput.split(',')
       # If extra commas are there do not take empty string
       if '' in newJobs:
           newJobs.remove('')
       if '' in newServers:
           newServers.remove('')
       loadBalance(newJobs, newServers, ring, distribution);

def processInput(jobString, serverString, ring, distribution):

    '''
    This method gets called directly from the unittest module
    Used mainly for unit testing.
    '''

    if jobString == '' or serverString == '':
	   print("Empty input encountered. Try again")
           return
    newJobs = jobString.split(',')
    newServers = serverString.split(',')
    # If extra commas are there do not take empty string
    if '' in newJobs:
        newJobs.remove('')
    if '' in newServers:
        newServers.remove('')
    loadBalance(newJobs, newServers, ring, distribution);


if __name__ == "__main__":
    try:
        goInteractive()
    except:
        print("Exception encountered while running the app")
        traceback.print_exc(file=sys.stdout)


