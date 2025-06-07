import smblueprint as sm
from .equals import equals

class memory_write:
    def __init__(self, bp, mem, address, inverted_address=None, x=0, y=0, z=0):
        # if the memory has only one address, we can write directly to it
        if mem.addresses == 1:
            address = 0

        self.trigger = sm.LogicGate(x, y, z, sm.LogicMode.OR, "00FF00")
        bp.add(self.trigger)

        self.input = [sm.LogicGate(x, y, z, sm.LogicMode.OR, "FFFFFF") for i in range(mem.bits)]
        for bit in self.input:
            bp.add(bit)

        if isinstance(address, int) and inverted_address is None: # Static addressing
            difference_line = [sm.LogicGate(x, y, z, sm.LogicMode.XOR, "88FF88") for i in range(mem.bits)]
            for bit in difference_line:
                bp.add(bit)

            flip_line = [sm.LogicGate(x, y, z, sm.LogicMode.AND, "88FF88") for i in range(mem.bits)]
            for bit in flip_line:
                bp.add(bit)

            for i in range(mem.bits):
                # Connect the input and the memory data to the difference line to find the bits that need to be flipped
                self.input[i].connect_to(difference_line[i])
                mem.data[address][i].connect_to(difference_line[i])

                # Connect the difference line to the write line
                difference_line[i].connect_to(flip_line[i])

                # Connect the trigger to the write line
                self.trigger.connect_to(flip_line[i])

                # Connect the write line to the memory data bits
                flip_line[i].connect_to(mem.data[address][i])


        elif isinstance(address, list) and isinstance(inverted_address, list): # Dynamic addressing
            difference_lines = [[sm.LogicGate(x, y, z, sm.LogicMode.XOR, "88FF88") for j in range(mem.bits)] for i in range(mem.addresses)]
            for line in difference_lines:
                for bit in line:
                    bp.add(bit)
            
            flip_lines = [[equals(bp,address,i,inverted_address,x,y,z).output for j in range(mem.bits)] for i in range(mem.addresses)]
            
            for i in range(mem.addresses):
                for j in range(mem.bits):
                    # Connect the input and the memory data to the difference line to find the bits that need to be flipped
                    self.input[j].connect_to(difference_lines[i][j])
                    mem.data[i][j].connect_to(difference_lines[i][j])

                    # Connect the difference line to the write line
                    difference_lines[i][j].connect_to(flip_lines[i][j])

                    # Connect the trigger to the write line
                    self.trigger.connect_to(flip_lines[i][j])

                    # Connect the write line to the memory data bits
                    flip_lines[i][j].connect_to(mem.data[i][j])
        else:
            raise ValueError("Address must be an integer or a list of inputs, and inverted_address must be provided if address is a list.")