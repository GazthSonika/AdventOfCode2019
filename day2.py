from utils import load
from numba import njit, prange

class A():
    def __init__(self, opcodes, idx=0):
        self.opcodes = opcodes[:]
        self.update_opcodes(12, 2)        
        self.idx = 0

    
    def update_opcodes(self, a, b):
        self.opcodes[1] = a
        self.opcodes[2] = b

    
    def op_1(self):
        i, o = self.idx, self.opcodes        
        o[o[i+3]] = o[o[i+1]] + o[o[i+2]]      
        self.idx += 4 
        return self
    
    def op_2(self):
        i, o = self.idx, self.opcodes
        o[o[i+3]] = o[o[i+1]] * o[o[i+2]]       
        self.idx += 4 
        return self

    def op_99(self):
        return False

    
    def run(self):                
        while self.opcodes[self.idx] != 99:            
            if self.opcodes[self.idx] == 1:
                self.op_1()
            elif self.opcodes[self.idx] == 2:
                self.op_2()            

        return self.opcodes[0]


def B(data, answer=19690720):            
    #brute force for the win! ;)
    for i in range(10000):
        a = A(data)
        params = i//100, i%100        
        a.update_opcodes(*params)
        if a.run() == answer:
            return params

    return None    


def main():
    data = [int(d) for d in load('day2_a.txt', ',')]    
    a = A(data)
    print(
        "A:", a.run(),
        "\nB", B(data)
    )        


if __name__ == "__main__":
    main()