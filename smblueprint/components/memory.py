import smblueprint as sm
import math

class memory:
    """
    A memory component that can store and retrieve data.
    The memory is implemented as a 2D array of flip-flops, where each address can store a specified number of bits.
    """
    def __init__(self, bp, addresses, bits, x=0, y=0, z=0):
        # Determine the number of address bits needed
        address_bits = math.ceil(math.log2(addresses))
        self.address_bits = address_bits
        self.addresses = addresses
        self.bits = bits

        # Create the memory
        self.data = [[sm.LogicGate(x, y, z, sm.LogicMode.XOR) for i in range(bits)] for j in range(addresses)]
        for address in self.data:
            for bit in address:
                bp.add(bit)
                bit.connect_to(bit) #Selfire to create a flip-flop