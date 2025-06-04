import smblueprint as sm
from .equals import equals

class memory_flip:
    def __init__(self, bp, mem, address, inverted_address, x=0, y=0, z=0):

        # Create the mask which only allows input to the bits of the memory at the given address
        mask = [[equals(bp,address,i,inverted_address,x,y,z).output for j in range(mem.bits)] for i in range(mem.addresses)]
        for i in range(mem.addresses):
            for j in range(mem.bits):
                bp.add(mask[i][j])
                mask[i][j].connect_to(mem.data[i][j])
                
        self.input = [sm.LogicGate(x, y, z, sm.LogicMode.OR) for i in range(mem.bits)]
        for j in range(mem.bits):
            bp.add(self.input[j])
            for i in range(mem.addresses):
                self.input[j].connect_to(mask[i][j])