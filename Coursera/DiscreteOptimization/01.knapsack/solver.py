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
        self.items = sorted(self.items, key = lambda x : -float(x.value)/x.weight)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class KnapzakOptimisticBounding(KnapzakGreedyDensity):    
    def __init__(self, input_data) :
        KnapzakGreedyDensity.__init__(self, input_data)
        self.Step = namedtuple("Step", ["idx", "weight", "value", "taken"])
    
    def getOptimisticSolution(self, start, capacity) :
        if capacity == -1 :
            capacity = self.capacity
        v = 0
        w = 0
        for i in range(start, self.numItems) :
            if w + self.items[i].weight > self.capacity :
                return v + float(self.capacity - w)*self.items[i].value/self.items[i].weight
            else :
                w += self.items[i].weight
                v += self.items[i].value
        return v
        
    def stepHeuristics(self, step) :
        return step.value + self.getOptimisticSolution(step.idx, self.capacity - step.weight)

    def _solve(self, idx, weight, value) :        
        # Check solution again optimistic value
        if idx < 0 :
            ov0 = self.getOptimisticSolution(0, self.capacity)
            ov1 = ov0
            idx = -1
        else :
            ov0 = value + self.getOptimisticSolution(idx+1, self.capacity - weight)
            ov1 = value + self.items[idx+1].value + self.getOptimisticSolution(idx+1, self.capacity - weight - self.items[idx+1].weight)
            
        if ov1 >= ov0 :
            if ov1 >= self.bestValue and weight + self.items[idx+1].weight <= self.capacity :
                self.steps.append(self.Step(idx + 1, weight + self.items[idx+1].weight, value + self.items[idx+1].value, 1))
            if ov0 >= self.bestValue and weight <= self.capacity :
                self.steps.append(self.Step(idx + 1, weight, value, 0))
        else :
            if ov0 >= self.bestValue and weight <= self.capacity :
                self.steps.append(self.Step(idx + 1, weight, value, 0))
            if ov1 >= self.bestValue and weight + self.items[idx+1].weight <= self.capacity :
                self.steps.append(self.Step(idx + 1, weight + self.items[idx+1].weight, value + self.items[idx+1].value, 1))

    def solve(self) :        
        self.sort()
        #print [float(i.value)/i.weight for i in self.items]
        #print self.items
        self.wayCounter = 0
        
        self.bestValue = 0
        self.bestTaken = 0        
                
        self.steps = []                
        self._solve(-1, 0, 0)
        while self.steps :            
            step = self.steps.pop()
            # print step

            self.wayCounter += 1
            if self.wayCounter > 1000000:
                continue
            
            self.taken[step.idx] = step.taken
            
            if step.idx == self.numItems-1 or step.weight == self.capacity:
                if step.value > self.bestValue :
                    self.bestValue = step.value
                    self.bestTaken = self.taken[:]
                continue
            
            self._solve(step.idx, step.weight, step.value)
        
        for i in range(self.numItems) :
            self.taken[self.items[i].index] = self.bestTaken[i]
         
        self.value = self.bestValue

class KnapzakOptimisticBounding2(KnapzakOptimisticBounding):    
    def __init__(self, input_data) :
        KnapzakGreedyDensity.__init__(self, input_data)
        self.Step = namedtuple("Step", ["idx", "weight", "value", "taken", "trust"])
    
    def getOptimisticSolution(self, start, capacity) :
        if capacity == -1 :
            capacity = self.capacity
        v = 0
        w = 0
        for i in range(start, self.numItems) :
            if w + self.items[i].weight > self.capacity :
                return v + float(self.capacity - w)*self.items[i].value/self.items[i].weight
            else :
                w += self.items[i].weight
                v += self.items[i].value
        return v
        
    def stepHeuristics(self, step) :
        return step.value + self.getOptimisticSolution(step.idx, self.capacity - step.weight)

    def _solve(self, idx, weight, value, trust) :        
        # Check solution again optimistic value
        if idx < 0 :
            ov0 = self.getOptimisticSolution(0, self.capacity)
            ov1 = ov0
            idx = -1
        else :
            ov0 = value + self.getOptimisticSolution(idx+1, self.capacity - weight)
            ov1 = value + self.items[idx+1].value + self.getOptimisticSolution(idx+1, self.capacity - weight - self.items[idx+1].weight)
            
        if ov1 >= ov0 :
            if ov1 >= self.bestValue and weight + self.items[idx+1].weight <= self.capacity :
                self.steps.append(self.Step(idx + 1, weight + self.items[idx+1].weight, value + self.items[idx+1].value, 1, trust))
            if ov0 >= self.bestValue and weight <= self.capacity and trust > 0:
                self.steps.append(self.Step(idx + 1, weight, value, 0, trust - 1))
        else :
            if ov0 >= self.bestValue and weight <= self.capacity :
                self.steps.append(self.Step(idx + 1, weight, value, 0, trust))
            if ov1 >= self.bestValue and weight + self.items[idx+1].weight <= self.capacity and trust > 0 :
                self.steps.append(self.Step(idx + 1, weight + self.items[idx+1].weight, value + self.items[idx+1].value, 1, trust - 1))

    def solve(self) :        
        self.sort()
        #print [float(i.value)/i.weight for i in self.items]
        #print self.items
        self.wayCounter = 0
        
        self.bestValue = 0
        self.bestTaken = 0        

        for trust_level in range(self.numItems+1) :
            
            print trust_level
            
            self.steps = []                
            self._solve(-1, 0, 0, trust_level)
            while self.steps :            
                step = self.steps.pop()
                # print step

                self.wayCounter += 1
                if self.wayCounter > 10000000:
                    break
            
                self.taken[step.idx] = step.taken
            
                if step.idx == self.numItems-1 or step.weight == self.capacity:
                    if step.value > self.bestValue :
                        self.bestValue = step.value
                        self.bestTaken = self.taken[:]
                    continue    
            
                self._solve(step.idx, step.weight, step.value, step.trust)                
        
            if self.wayCounter > 10000000:
                break
                    
        for i in range(self.numItems) :
            self.taken[self.items[i].index] = self.bestTaken[i]
         
        self.value = self.bestValue
        

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    # knapzak = KnapzakGreedyDensity(input_data)
    knapzak = KnapzakOptimisticBounding2(input_data)
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

