import smblueprint as sm
import math

class memory:
    def __init__(self, bp, addresses, bits, x=0, y=0, z=0):
        # Determine the number of address bits needed
        address_bits = math.ceil(math.log2(addresses))

        # Create the memory
        data = [[sm.LogicGate(x, y, z, sm.LogicMode.XOR) for i in range(bits)] for j in range(addresses)]
        for address in data:
            for bit in address:
                bp.add_gate(bit)
                bit.connect_to(bit) #Selfire to create a flip-flop
        
        # Create the input gates
        input_address = [sm.LogicGate(x+i, y, z+1, sm.LogicMode.OR) for i in range(address_bits)]
        for bit in input_address:
            bp.add_gate(bit)
        self.input_address = input_address

        # Create inverted input address gates for querying if a specific address is selected
        inverted_input_address = [sm.LogicGate(x, y, z, sm.LogicMode.NOR) for i in range(address_bits)]
        for i in range(address_bits):
            bp.add_gate(inverted_input_address[i])
            self.input_address[i].connect_to(inverted_input_address[i])

        # Create the input data gates
        data_in = [sm.LogicGate(x+i, y+1, z+1, sm.LogicMode.OR) for i in range(bits)]
        for bit in data_in:
            bp.add_gate(bit)
        self.data_in = data_in

        # Create the data output gates which output the data from the selected address
        data_out = [sm.LogicGate(x+i, y+2, z+1, sm.LogicMode.OR) for i in range(bits)]
        for bit in data_out:
            bp.add_gate(bit)
        self.data_out = data_out

        # Created masked output gates that will output the data from the selected address only when the address is selected
        masked_outs = [[sm.LogicGate(x, y, z, sm.LogicMode.AND) for i in range(bits)] for j in range(addresses)]
        for address in range(addresses):
            for bit in range(bits):
                bp.add_gate(masked_outs[address][bit])

                # Connect the data to the corresponding masked output gate
                data[address][bit].connect_to(masked_outs[address][bit])

                # Connect the masked output to the data output gate
                masked_outs[address][bit].connect_to(data_out[bit])

                # Mask the output with a combination of the input address and the inverted input address
                for i in range(address_bits):
                    if (address >> i) & 1:
                        input_address[i].connect_to(masked_outs[address][bit])
                    else:
                        inverted_input_address[i].connect_to(masked_outs[address][bit])

        # Connect the write gate to the data input gates
        masked_ins = [[sm.LogicGate(x, y, z, sm.LogicMode.AND) for i in range(bits)] for j in range(addresses)]
        for address in range(addresses):
            for bit in range(bits):
                bp.add_gate(masked_ins[address][bit])

                # Connect the data input to the corresponding masked input gate
                data_in[bit].connect_to(masked_ins[address][bit])

                # Connect the masked input to the data at the selected address
                masked_ins[address][bit].connect_to(data[address][bit])

                # Mask the input with a combination of the input address and the inverted input address
                for i in range(address_bits):
                    if (address >> i) & 1:
                        input_address[i].connect_to(masked_ins[address][bit])
                    else:
                        inverted_input_address[i].connect_to(masked_ins[address][bit])