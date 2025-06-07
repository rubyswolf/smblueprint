import smblueprint as sm
from .equals import equals
import math

class rom:
    def __init__(self, bp, address, inverted_address, bits, data, x=0, y=0, z=0):
        if isinstance(data, list): # List of values
            self.addresses = len(data)
        elif isinstance(data, dict): # Sparse dictionary
            # Find the maximum address
            self.addresses = max(list(data.keys()))+1
        else:
            raise ValueError("Data must be a list or a dictionary.")
        
        address_bits = math.ceil(math.log2(self.addresses))
        if address_bits > len(address):
            raise ValueError(f"Address input of size {len(address)} is not big enough to point to all {self.addresses} addresses in the data, required size is {address_bits}.")
        
        if isinstance(data, list): # List of values
            address_decoder = [equals(bp, address, i, inverted_address, x, y, z).output for i in range(self.addresses)]
        elif isinstance(data, dict): # Sparse dictionary
            address_decoder = {i: equals(bp, address, i, inverted_address, x, y, z).output for i in data.keys()}
        
        self.output = [sm.LogicGate(x, y, z, sm.LogicMode.OR, "00FFFF") for i in range(bits)]
        for bit in self.output:
            bp.add(bit)

        if isinstance(data, list):
            for i in range(self.addresses):
                for j in range(bits):
                    if (data[i] >> j) & 1:
                        address_decoder[i].connect_to(self.output[j])
        elif isinstance(data, dict):
            for i in data.keys():
                for j in range(bits):
                    if (data[i] >> j) & 1:
                        address_decoder[i].connect_to(self.output[j])
        
