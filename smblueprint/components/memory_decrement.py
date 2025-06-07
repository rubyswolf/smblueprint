import smblueprint as sm
from .equals import equals

class memory_decrement:
    """
    A component to decrement the value of a memory cell by 1
    Addresses can be an integer for static addressing or a list of gates for dynamic addressing.
    if gated is True, the decrement will only occur when the the gate is on
    """
    def __init__(self, bp, mem, gated, address, inverted_address=None, x=0, y=0, z=0):
        if mem.addresses == 1: # If there is only one address
            address = 0 # Target the only address available without needing to select it

        if gated:
            # If the decrement is gated, we need to create a gate for the decrement
            self.gate = sm.LogicGate(x, y, z, sm.LogicMode.OR, "000000")
            bp.add(self.gate)

        if isinstance(address, int) and inverted_address is None: # Static addressing
            # Trigger to decrement the memory
            self.trigger = sm.LogicGate(x, y, z, sm.LogicMode.NOR, "0000FF")
            bp.add(self.trigger)

            # If the addressing is static, we only need one decrement line
            decrement_line = [sm.LogicGate(x, y, z, sm.LogicMode.NOR, "8888FF") for i in range(mem.bits)]
            for bit in decrement_line:
                bp.add(bit)

            if gated:
                gated_decrement_line = [sm.LogicGate(x, y, z, sm.LogicMode.AND, "8888FF") for i in range(mem.bits)]
                for bit in gated_decrement_line:
                    bp.add(bit)

            for i in range(mem.bits):
                # Hook up the decrement lines to the memory data bits
                if gated:
                    decrement_line[i].connect_to(gated_decrement_line[i])
                    gated_decrement_line[i].connect_to(mem.data[address][i])
                    self.gate.connect_to(gated_decrement_line[i])
                else:
                    decrement_line[i].connect_to(mem.data[address][i])
                self.trigger.connect_to(decrement_line[i])

                for j in range(mem.bits-i-1):
                    mem.data[address][j].connect_to(decrement_line[i+j+1])
        elif isinstance(address, list) and isinstance(inverted_address, list): # Dynamic addressing
            # Trigger to decrement the memory
            self.trigger = sm.LogicGate(x, y, z, sm.LogicMode.OR, "0000FF")
            bp.add(self.trigger)

            # Create a set of triggers for each address that only trigger when the address matches
            trigger_line = [equals(bp,address,i,inverted_address,x,y,z).output for i in range(mem.addresses)]

            for trigger in trigger_line:
                # Connect the main trigger to each of the address trigger lines
                trigger.mode = sm.LogicMode.NAND  # Ensure the trigger lines are NAND gates
                self.trigger.connect_to(trigger)

            # If the addressing is dynamic, we need to create an decrement line for each address
            decrement_lines = [[sm.LogicGate(x, y, z, sm.LogicMode.NOR, "8888FF") for i in range(mem.bits)] for j in range(mem.addresses)]
            for line in decrement_lines:
                for bit in line:
                    bp.add(bit)

            if gated:
                gated_decrement_lines = [[sm.LogicGate(x, y, z, sm.LogicMode.AND, "8888FF") for i in range(mem.bits)] for j in range(mem.addresses)]
                for line in gated_decrement_lines:
                    for bit in line:
                        bp.add(bit)
            
            for i in range(mem.addresses):
                for j in range(mem.bits):
                    # Hook up the decrement lines to the memory data bits
                    if gated:
                        decrement_lines[i][j].connect_to(gated_decrement_lines[i][j])
                        gated_decrement_lines[i][j].connect_to(mem.data[i][j])
                        self.gate.connect_to(gated_decrement_lines[i][j])
                    else:
                        decrement_lines[i][j].connect_to(mem.data[i][j])
                    trigger_line[i].connect_to(decrement_lines[i][j])

                    for k in range(mem.bits-j-1):
                        mem.data[i][k].connect_to(decrement_lines[i][j+k+1])
        else:
            raise ValueError("Address must be an integer or a list of inputs, and inverted_address must be provided if address is a list.")