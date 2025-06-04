import smblueprint as sm

class counter:
    def __init__(self, bp, bits, include_decrement=True, x=0, y=0, z=0):
        self.increment = sm.LogicGate(x, y, z, sm.LogicMode.OR, "FF0000")
        bp.add_gate(self.increment)

        if include_decrement:
            self.decrement = sm.LogicGate(x, y, z, sm.LogicMode.NOR, "0000FF")
            bp.add_gate(self.decrement)

        data = [sm.LogicGate(x, y, z, sm.LogicMode.XOR) for i in range(bits)]
        for bit in data:
            bp.add_gate(bit)
            bit.connect_to(bit)
        self.output = data

        increment_line = [sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF8888") for i in range(bits)]
        for bit in increment_line:
            bp.add_gate(bit)

        if include_decrement:
            decrement_line = [sm.LogicGate(x, y, z, sm.LogicMode.NOR, "8888FF") for i in range(bits)]
            for bit in decrement_line:
                bp.add_gate(bit)

        for i in range(bits):
            increment_line[i].connect_to(data[i])
            self.increment.connect_to(increment_line[i])
            if include_decrement:
                decrement_line[i].connect_to(data[i])
                self.decrement.connect_to(decrement_line[i])

            for j in range(bits-i-1):
                data[i].connect_to(increment_line[i+j+1])
                if include_decrement:
                    data[i].connect_to(decrement_line[i+j+1])