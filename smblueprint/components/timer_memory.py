import smblueprint as sm
from .memory import memory
from .memory_increment import memory_increment
from .memory_read import memory_read

class timer_memory:
    def __init__(self, bp, size, bits, x=0, y=0, z=0):
        self.addresses = 2**size # Number of addresses is 2^size
        self.bits = bits # Number of bits per address
        
        self.timers = [sm.Timer(x, y, z, self.addresses) for i in range(bits)]
        self.resets = [sm.LogicGate(x, y, z, sm.LogicMode.AND, "000000") for i in range(bits)]
        self.sets = [sm.LogicGate(x, y, z, sm.LogicMode.OR, "FFFFFF") for i in range(bits)]
        for i in range(bits):
            bp.add(self.timers[i])
            bp.add(self.sets[i])
            bp.add(self.resets[i])
            self.timers[i].connect_to(self.resets[i])
            self.resets[i].connect_to(self.sets[i])
            self.sets[i].connect_to(self.timers[i])
        
        self.counter = memory(bp, 1, self.addresses, x, y, z)
        memory_increment(bp, self.counter, False, 1, None, x, y, z).trigger
        