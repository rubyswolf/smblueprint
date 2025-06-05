import smblueprint as sm
from .memory import memory
from .memory_read import memory_read
from .memory_write import memory_write
from .memory_increment import memory_increment
from .memory_decrement import memory_decrement
from .memory_set import memory_set
from .invert import invert
class stack:
    """ 
    A stack data structure implemented using memory components.
    Clear on pop can be set to True to reset the memory address to 0 when popping a value.
    Note the pointer moves AND THEN writes, so that the pointed value is the top of the stack.
    This means that the first value of the stack is at memory address 1, because the pointer starts at 0.
    If you want the stack to start at 0, manually set the pointer to the highest address of the stack so it wraps around to 0.
    """
    def __init__(self, bp, size, bits, poppable=True, clear_on_pop=False, x=0, y=0, z=0):
        # Push and pop inputs
        self.push = sm.LogicGate(x, y, z, sm.LogicMode.AND, "00FF00")
        bp.add(self.push)

        if poppable:
            self.pop = sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF00FF")
            bp.add(self.pop)

        # Memory to hold stack data
        self.memory = memory(bp, size, bits, x, y, z)

        # Stack pointer to track the top of the stack
        self.pointer = memory(bp, 1, self.memory.address_bits, x, y, z)

        # Make the stack pointer into a counter
        pointer_incrementer = memory_increment(bp, self.pointer, True, 0, None, x, y, z)
        if poppable:
            pointer_decrementer = memory_decrement(bp, self.pointer, True, 0, None, x, y, z)

        if poppable:
            # Merge their gates and expose it
            bp.merge(pointer_incrementer.gate, pointer_decrementer.gate)
        self.gate = pointer_incrementer.gate
        self.gate.connect_to(self.push)
        
        if poppable:
            self.gate.connect_to(self.pop)

        # Get the pointer value
        pointer_value = self.pointer.data[0]
        inverted_pointer_value = invert(bp, pointer_value, x, y, z).output

        # Create a read head for the stack at the pointer position
        mem_read = memory_read(bp, self.memory, pointer_value, inverted_pointer_value, x, y, z)

        # Output for the current top of the stack
        self.output = mem_read.output

        # Write head for the stack at the pointer position
        mem_write = memory_write(bp, self.memory, pointer_value, inverted_pointer_value, x, y, z)
        self.input = mem_write.input

        # Handle push operation
        self.push.connect_to(pointer_incrementer.trigger)
        write_delay = sm.Timer(x, y, z, 3)
        bp.add(write_delay)

        self.push.connect_to(write_delay)
        write_delay.connect_to(mem_write.trigger)

        # Handle pop operation
        if poppable:
            if clear_on_pop:
                # If we want to clear the popped value
                mem_set = memory_set(bp, self.memory, pointer_value, 0, inverted_pointer_value, x, y, z)
                self.pop.connect_to(mem_set.trigger)

            self.pop.connect_to(pointer_decrementer.trigger)




        