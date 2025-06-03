import smblueprint as sm

class decoder:
    def __init__(self, bp, bits, x=0, y=0, z=0):
        self.input = [sm.LogicGate(x+i, y, z, sm.LogicMode.OR) for i in range(bits)]
        for i in range(bits):
            bp.add_gate(self.input[i])
        inverted = [sm.LogicGate(x, y+1, z, sm.LogicMode.NOR) for i in range(bits)]
        for i in range(bits):
            bp.add_gate(inverted[i])
            self.input[i].connect_to(inverted[i])
        values = 2**bits
        self.output = [sm.LogicGate(x, y+1, z, sm.LogicMode.AND) for i in range(values)]
        for i in range(values):
            bp.add_gate(self.output[i])
            for j in range(bits):
                if (i >> j) & 1:
                    self.input[j].connect_to(self.output[i])
                else:
                    inverted[j].connect_to(self.output[i])