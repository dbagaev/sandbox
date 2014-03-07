#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

class KnapzakBase :
    def __init__(self, input_data) :
        # parse the input
        lines = input_data.split('\n')

        firstLine = lines[0].split()
        self.item_count = int(firstLine[0])
        self.capacity = int(firstLine[1])

        self.items = []

        i = 0
        for line in lines[1:] :
            parts = line.split()
            if len(parts) < 2 :
                continue
            self.items.append(Item(i, int(parts[0]), int(parts[1])))
            i += 1

        # Init knapzak values
        self.value = 0
        self.weight = 0
        self.taken = [0]*len(self.items)
            
    def getOutput(self) :
        # prepare the solution in the specified output format
        output_data = str(self.value) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, self.taken))
        return output_data
        
class KnapzakTrivialGreedy(KnapzakBase) :
    def sort(self):
        # a trivial greedy algorithm for filling the knapsack
        # it takes items in-order until the knapsack is full
        return
        
    def solve(self) :
        self.sort()
        for item in self.items:
            if self.weight + item.weight <= self.capacity:
                self.taken[item.index] = 1
                self.value += item.value
                self.weight += item.weight

class KnapzakGreedyDensity(KnapzakTrivialGreedy) :    
    def sort(self):
        # a trivial greedy algorithm for filling the knapsack
        # it takes items in-order until the knapsack is full
        self.items = sorted(self.items, key = lambda x : x.value/x.weight)
                
def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    knapzak = KnapzakGreedyDensity(input_data)
    knapzak.solve()
    return knapzak.getOutput()

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

