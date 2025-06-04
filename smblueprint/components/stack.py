import smblueprint as sm
import math
from .counter import counter
from .writable_memory import writable_memory

class stack:
    def __init__(self, bp, size, bits, x=0, y=0, z=0):     
        self.push = sm.LogicGate(x+1, y, z, sm.LogicMode.OR, "00FF00")
        bp.add(self.push)

        self.pop = sm.LogicGate(x+2, y, z, sm.LogicMode.OR, "FF00FF")
        bp.add(self.pop)

        # Create memory for the stack
        mem = writable_memory(bp, size, bits, x, y, z)
        self.input = mem.write_input
        for i in range(bits):
            self.input[i].pos["x"] += i
            self.input[i].pos["y"] += 1
            mem.memory.data_out[i].pos["x"] += i
            mem.memory.data_out[i].pos["y"] += 2

        self.output = mem.memory.data_out
        
        # Create a counter to keep track of the stack pointer
        pointer = counter(bp, mem.memory.address_bits, True, x, y, z)

        self.push.connect_to(mem.trigger_write)
        increment_delay = sm.LogicGate(x, y, z, sm.LogicMode.OR)
        bp.add(increment_delay)
        self.push.connect_to(increment_delay)
        increment_delay.connect_to(pointer.increment)

        self.pop.connect_to(pointer.decrement)

        # Connect the counter to the memory address input
        for i in range(mem.memory.address_bits):
            pointer.output[i].connect_to(mem.memory.input_address[i])