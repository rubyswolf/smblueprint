import smblueprint as sm

class rising_edge:
    """Detects a rising edge on the input signal."""
    def __init__(self, bp, input, x=0, y=0, z=0):
        was_off = sm.LogicGate(x, y, z, sm.LogicMode.NOR) # This gate checks if the input was off a tick ago
        bp.add(was_off)
        input.connect_to(was_off)

        self.output = sm.LogicGate(x, y, z, sm.LogicMode.AND) # This gate outputs a signal when the input goes from off to on
        bp.add(self.output)

        # If the input was off and now is on, the output will be on for one tick
        input.connect_to(self.output)
        was_off.connect_to(self.output)
