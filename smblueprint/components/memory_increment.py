import smblueprint as sm
from .equals import equals

class memory_increment:
    """
    A component to increment the value of a memory cell by 1
    Addresses can be an integer for static addressing or a list of gates for dynamic addressing.
    if gated is True, the increment will only occur when the the gate is on
    """
    def __init__(self, bp, mem, gated, address, inverted_address=None, x=0, y=0, z=0):
        if mem.addresses == 1: # If there is only one address
            address = 0 # Target the only address available without needing to select it

        # Trigger to increment the memory
        self.trigger = sm.LogicGate(x, y, z, sm.LogicMode.OR, "FF0000")
        bp.add(self.trigger)

        if gated:
            # If the increment is gated, we need to create a gate for the increment
            self.gate = sm.LogicGate(x, y, z, sm.LogicMode.OR, "000000")
            bp.add(self.gate)

        if isinstance(address, int) and inverted_address is None: # Static addressing
            # If the addressing is static, we only need one increment line
            increment_line = [sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF8888") for i in range(mem.bits)]
            for bit in increment_line:
                bp.add(bit)

            if gated:
                gated_increment_line = [sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF8888") for i in range(mem.bits)]
                for bit in gated_increment_line:
                    bp.add(bit)

            for i in range(mem.bits):
                # Hook up the increment lines to the memory data bits
                if gated:
                    increment_line[i].connect_to(gated_increment_line[i])
                    gated_increment_line[i].connect_to(mem.data[address][i])
                    self.gate.connect_to(gated_increment_line[i])
                else:
                    increment_line[i].connect_to(mem.data[address][i])
                
                self.trigger.connect_to(increment_line[i])

                for j in range(mem.bits-i-1):
                    mem.data[address][j].connect_to(increment_line[i+j+1])
        elif isinstance(address, list) and isinstance(inverted_address, list): # Dynamic addressing
            # Create a set of triggers for each address that only trigger when the address matches
            trigger_line = [equals(bp,address,i,inverted_address,x,y,z).output for i in range(mem.addresses)]

            for trigger in trigger_line:
                # Connect the main trigger to each of the address trigger lines
                self.trigger.connect_to(trigger)

            # If the addressing is dynamic, we need to create an increment line for each address
            increment_lines = [[sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF8888") for i in range(mem.bits)] for j in range(mem.addresses)]
            for line in increment_lines:
                for bit in line:
                    bp.add(bit)
            
            if gated:
                gated_increment_lines = [[sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF8888") for i in range(mem.bits)] for j in range(mem.addresses)]
                for line in gated_increment_lines:
                    for bit in line:
                        bp.add(bit)
            
            for i in range(mem.addresses):
                for j in range(mem.bits):
                    # Hook up the increment lines to the memory data bits
                    if gated:
                        increment_lines[i][j].connect_to(gated_increment_lines[i][j])
                        gated_increment_lines[i][j].connect_to(mem.data[i][j])
                        self.gate.connect_to(gated_increment_lines[i][j])
                    else:
                        increment_lines[i][j].connect_to(mem.data[i][j])

                    trigger_line[i].connect_to(increment_lines[i][j])

                    for k in range(mem.bits-j-1):
                        mem.data[i][k].connect_to(increment_lines[i][j+k+1])
        else:
            raise ValueError("Address must be an integer or a list of inputs, and inverted_address must be provided if address is a list.")