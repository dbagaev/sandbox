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
        self.numItems = len(self.items)

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

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class KnapzakGreedyDensity(KnapzakTrivialGreedy) :    
    def sort(self):
        self.items = sorted(self.items, key = lambda x : x.value/x.weight)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class KnapzakOptimisticBounding(KnapzakGreedyDensity):
    
    def getOptimisticSolution(self, start = 0, capacity = -1) :
        if capacity == -1 :
            capacity = self.capacity
        v = 0
        w = 0
        for i in range(start, self.numItems) :
            if w + self.items[i].weight > self.capacity :
                return v + (self.capacity - w)*self.items[i].value/self.items[i].weight
            else :
                w += self.items[i].weight
                v += self.items[i].value
        return v

    def _solve(self, idx, weight, value) :
        self.wayCounter += 1
        if weight > self.capacity or self.wayCounter > 1000000:
            return
            
        if idx == self.numItems :
            if value > self.bestValue :
                self.bestValue = value
                self.bestTaken = self.taken[:]
            return
            
        # Check solution again optimistic value
        ov0 = value + self.getOptimisticSolution(idx+1, self.capacity - weight)
        ov1 = value + self.items[idx].value + self.getOptimisticSolution(idx+1, self.capacity - weight - self.items[idx].weight)
        
        if ov1 > ov0 :
            if ov1 > self.bestValue :
                self.taken[idx] = 1
                self._solve(idx + 1, weight + self.items[idx].weight, value + self.items[idx].value)
            if ov0 > self.bestValue :
                self.taken[idx] = 0
                self._solve(idx + 1, weight, value)
        else :
            if ov0 > self.bestValue :
                self.taken[idx] = 0
                self._solve(idx + 1, weight, value)
            if ov1 > self.bestValue :
                self.taken[idx] = 1
                self._solve(idx + 1, weight + self.items[idx].weight, value + self.items[idx].value)

    def solve(self) :
        self.sort()
        self.wayCounter = 0
        
        self.bestValue = 0
        self.bestTaken = 0        
        
        self._solve(0, 0, 0)
        
        self.taken = self.bestTaken[:]
        self.value = self.bestValue


def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    knapzak = KnapzakOptimisticBounding(input_data)
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

