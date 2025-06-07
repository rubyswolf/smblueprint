import smblueprint as sm
from .rising_edge import rising_edge

class falling_edge:
    """
    Detects a falling edge on the input signal by by finding the rising edge of the inverted input signal.
    """
    def __init__(self, bp, input, x=0, y=0, z=0):
        input_inverted = sm.LogicGate(x, y, z, sm.LogicMode.NOR)
        bp.add(input_inverted)
        input.connect_to(input_inverted)
        rise = rising_edge(bp, input_inverted, x, y, z)
        self.output = rise.output
