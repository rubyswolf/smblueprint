import smblueprint as sm

class dual_edge:
    """
    Detects both rising and falling edges on the input signal.
    """
    def __init__(self, bp, input, x=0, y=0, z=0):
        delayed = sm.LogicGate(x, y, z, sm.LogicMode.AND) # This gate checks if the input was on a tick ago
        bp.add(delayed)
        input.connect_to(delayed)

        self.output = sm.LogicGate(x, y, z, sm.LogicMode.XOR) # XOR checks if two inputs are different
        bp.add(self.output)

        # Check if the current input is different from the input from the previous tick
        input.connect_to(self.output)
        delayed.connect_to(self.output)