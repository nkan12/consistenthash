#!/usr/bin/python

import unittest
import lb
import json
import copy
import os
import utilities

OUTPUT_FILE_PATH = "./test_output"

outFile = None
oldDistribution = {}

class BehaviourTestCase(unittest.TestCase):

    def setUp(self):
        self.ring = lb.Ring();
        self.distribution = {}

    def testcase_1_populate_ring(self):
        '''
        Populate hash ring and check back
        '''
        self.assertEqual(self.ring.nodes, [])
        for entry in range(0,20):
            self.ring.addNode(str(entry))
        nodeList = [node.id for node in self.ring.nodes]
        
        self.assertEqual(len(nodeList), 3*len(range(0,20)))

    
    def testcase_2_more_server_than_jobs(self):
        '''
        More servers than jobs
        '''
        jobs = "0,1" 
        servers = "0,1,2" 
        lb.processInput(jobs, servers, self.ring, self.distribution)
        outFile.write("\n\ntestcase_2_check_more_servers_than_jobs \n")
        outFile.write("jobs:\n");
        outFile.write(json.dumps(jobs))
        outFile.write("\nservers: \n");
        outFile.write(json.dumps(servers))
        outFile.write("\ndistribution: \n");
        outFile.write(json.dumps(self.distribution))
        self.assertLess(len(self.distribution.keys()), len(servers))

    def testcase_3_check_distribution_22_5(self):
        global oldDistribution
        jobs = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22" 
        servers = "0,1,2,3,4" 
        lb.processInput(jobs, servers, self.ring, self.distribution)
        outFile.write("\n\ntestcase_3_check_distribution_22_5 \n")
        outFile.write("jobs:\n");
        outFile.write(json.dumps(jobs))
        outFile.write("\nservers: \n");
        outFile.write(json.dumps(servers))
        outFile.write("\ndistribution: \n");
        outFile.write(json.dumps(self.distribution))
        oldDistribution = copy.deepcopy(self.distribution)
        
    def testcase_4_check_distribution_22_4(self):
        '''
        Remove server 2 and check whether jobs moved from servers 0,1,3,4
        '''
        global oldDistribution
        jobs = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22" 
        servers = "0,1,3,4" 
        lb.processInput(jobs, servers, self.ring, self.distribution)
        outFile.write("\n\ntestcase_3_check_distribution_22_4 \n")
        outFile.write("jobs:\n");
        outFile.write(json.dumps(jobs))
        outFile.write("\nservers: \n");
        outFile.write(json.dumps(servers))
        outFile.write("\ndistribution: \n");
        outFile.write(json.dumps(self.distribution))
        noJobsMoved = utilities.getNoJobsMoved(oldDistribution, self.distribution)
        outFile.write("\nNoJobsMovedNodes: \n");
        outFile.write(json.dumps(noJobsMoved))
        oldDistribution = copy.deepcopy(self.distribution)
        outFile.write("\n")
        self.assertGreaterEqual(len(noJobsMoved), 3)
       
    def testcase_5_check_distribution_25_4(self):
        '''
        Add 2 more jobs and check whether existing jobs in 0,1,3,4 moved
        '''
        global oldDistribution
        jobs = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25" 
        servers = "0,1,3,4" 
        lb.processInput(jobs, servers, self.ring, self.distribution)
        outFile.write("\n\ntestcase_5_check_distribution_25_4 \n")
        outFile.write("jobs:\n");
        outFile.write(json.dumps(jobs))
        outFile.write("\nservers: \n");
        outFile.write(json.dumps(servers))
        outFile.write("\ndistribution: \n");
        outFile.write(json.dumps(self.distribution))
        noJobsMoved = utilities.getNoJobsMoved(oldDistribution, self.distribution)
        outFile.write("\nNoJobsMovedNodes: \n");
        outFile.write(json.dumps(noJobsMoved))
        oldDistribution = copy.deepcopy(self.distribution)
        outFile.write("\n")
        self.assertGreaterEqual(len(noJobsMoved), 3)
       
    def testcase_6_check_distribution_25_5(self):
        '''
        Add one more server 5 and check how many servers had jobs unmoved
        '''
        global oldDistribution
        jobs = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25" 
        servers = "0,1,3,4,5" 
        lb.processInput(jobs, servers, self.ring, self.distribution)
        outFile.write("\n\ntestcase_6_check_distribution_25_5 \n")
        outFile.write("jobs:\n");
        outFile.write(json.dumps(jobs))
        outFile.write("\nservers: \n");
        outFile.write(json.dumps(servers))
        outFile.write("\ndistribution: \n");
        outFile.write(json.dumps(self.distribution))
        noJobsMoved = utilities.getNoJobsMoved(oldDistribution, self.distribution)
        outFile.write("\nNoJobsMovedNodes: \n");
        outFile.write(json.dumps(noJobsMoved))
        oldDistribution = copy.deepcopy(self.distribution)
        outFile.write("\n")
        self.assertGreaterEqual(len(noJobsMoved), 3)

    def testcase_7_no_jobs(self):
        '''
        Empty jobs and servers
        '''
        global oldDistribution
        jobs = "" 
        servers = "" 
        lb.processInput(jobs, servers, self.ring, self.distribution)
        outFile.write("\n\ntestcase_7_no_jobs \n")
        outFile.write("jobs:\n");
        outFile.write(json.dumps(jobs))
        outFile.write("\nservers: \n");
        outFile.write(json.dumps(servers))
        outFile.write("\ndistribution: \n");
        outFile.write(json.dumps(self.distribution))
        noJobsMoved = utilities.getNoJobsMoved(oldDistribution, self.distribution)
        outFile.write("\nNoJobsMovedNodes: \n");
        self.assertEqual(len(self.distribution.keys()), 0)
        outFile.write(json.dumps(noJobsMoved))

    def tearDown(self):
        self.ring = None

if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILE_PATH):
        os.remove(OUTPUT_FILE_PATH)
    outFile = open(OUTPUT_FILE_PATH, "a+")
    unittest.main()
