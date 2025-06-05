import smblueprint as sm

class equals:
    def __init__(self, bp, input1, input2, input1_inverted=None, x=0, y=0, z=0):
        if isinstance(input2, int) and not input1_inverted is None: # Constant comparison
            # print(input1_inverted)
            # Create the output line
            self.output = sm.LogicGate(x, y, z, sm.LogicMode.AND, "FF0000")
            bp.add(self.output)

            for i in range(len(input1)):
                # Connect the input and inverted to the output according to the constant
                (input1[i] if (input2 >> i) & 1 else input1_inverted[i]).connect_to(self.output)
        elif isinstance(input2, list): # Two input comparison
            # Create a line of XOR gates to find the difference
            difference = [sm.LogicGate(x, y, z, sm.LogicMode.XOR) for i in range(len(input1))]
            for i in range(len(input1)):
                bp.add(difference[i])
                input1[i].connect_to(difference[i])
                input2[i].connect_to(difference[i])

            # Create a NOR gate to check if all bits have no difference
            self.output = sm.LogicGate(x, y, z, sm.LogicMode.NOR, "FF0000")
            bp.add(self.output)
            for i in range(len(input1)):
                difference[i].connect_to(self.output)
        else:
            raise ValueError("Input2 must be an integer or a list of inputs.")