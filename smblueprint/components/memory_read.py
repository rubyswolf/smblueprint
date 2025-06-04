import smblueprint as sm
from .equals import equals

class memory_read:
    def __init__(self, bp, mem, address, inverted_address, x=0, y=0, z=0):

        # Create the mask which only outputs the bits of the memory at the given address
        mask = [[equals(bp,address,i,inverted_address,x,y,z).output for j in range(mem.bits)] for i in range(mem.addresses)]
        for i in range(mem.addresses):
            for j in range(mem.bits):
                mem.data[i][j].connect_to(mask[i][j])

        self.output = [sm.LogicGate(x, y, z, sm.LogicMode.OR) for i in range(mem.bits)]
        for j in range(mem.bits):
            bp.add(self.output[j])
            for i in range(mem.addresses):
                mask[i][j].connect_to(self.output[j])