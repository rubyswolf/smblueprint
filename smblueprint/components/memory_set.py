import smblueprint as sm
from .equals import equals

class memory_set:
    def __init__(self, bp, mem, address, value, inverted_address=None, x=0, y=0, z=0):
        # if the memory has only one address, we can write directly to it
        if mem.addresses == 1:
            address = 0

        self.trigger = sm.LogicGate(x, y, z, sm.LogicMode.OR, "FF00FF")
        bp.add(self.trigger)

        if isinstance(address, int) and inverted_address is None: # Static addressing
            difference_line = [sm.LogicGate(x, y, z, sm.LogicMode.XNOR if value >> i & 1 else sm.LogicMode.XOR, "FF88FF") for i in range(mem.bits)]
            for bit in difference_line:
                bp.add(bit)
            
            flip_line = [sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF88FF") for i in range(mem.bits)]
            for bit in flip_line:
                bp.add(bit)
            
            for i in range(mem.bits):
                mem.data[address][i].connect_to(difference_line[i])
                difference_line[i].connect_to(flip_line[i])
                self.trigger.connect_to(flip_line[i])
                flip_line[i].connect_to(mem.data[address][i])
        elif isinstance(address, list) and isinstance(inverted_address, list): # Dynamic addressing
            difference_lines = [[sm.LogicGate(x, y, z, sm.LogicMode.XNOR if value >> j & 1 else sm.LogicMode.XOR, "FF88FF") for j in range(mem.bits)] for i in range(mem.addresses)]
            for line in difference_lines:
                for bit in line:
                    bp.add(bit)
            
            flip_lines = [[equals(bp,address,i,inverted_address,x,y,z).output for j in range(mem.bits)] for i in range(mem.addresses)]
            
            for i in range(mem.addresses):
                for j in range(mem.bits):
                    mem.data[i][j].connect_to(difference_lines[i][j])
                    difference_lines[i][j].connect_to(flip_lines[i][j])
                    self.trigger.connect_to(flip_lines[i][j])
                    flip_lines[i][j].connect_to(mem.data[i][j])