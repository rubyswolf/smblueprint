import smblueprint as sm

class invert:
    def __init__(self, bp, input_array, x=0, y=0, z=0):
        self.output = [sm.LogicGate(x, y, z, sm.LogicMode.NOR) for _ in range(len(input_array))]
        
        for i in range(len(input_array)):
            bp.add(self.output[i])
            input_array[i].connect_to(self.output[i])