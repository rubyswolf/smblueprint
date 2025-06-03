import json
from enum import IntEnum, Enum

class LogicMode(IntEnum):
    AND = 0
    OR = 1
    XOR = 2
    NAND = 3
    NOR = 4
    XNOR = 5


class LogicGate:
    def __init__(self, x, y, z, mode: LogicMode, color="DF7F01"):
        self.id = None  # ID will be assigned by Blueprint
        self.mode = mode
        self.color = color
        self.pos = {"x": x, "y": y, "z": z}
        self.controllers = []
        self.shapeId = "9f0f56e8-2c31-4d83-996c-d00a9b296c3f"
        self.xaxis = 2
        self.zaxis = 1

    def connect_to(self, target_gate):
        self.controllers.append({"id": target_gate.id})

    def to_dict(self):
        return {
            "color": self.color,
            "controller": {
                "id": self.id,
                "mode": self.mode,
                "active": False,
                "controllers": self.controllers or None,
                "joints": None
            },
            "pos": self.pos,
            "shapeId": self.shapeId,
            "xaxis": self.xaxis,
            "zaxis": self.zaxis
        }


class BlockType(Enum):
    PLASTIC = "628b2d61-5ceb-43e9-8334-a4135566df7a"
    METAL1 = "8aedf6c2-94e1-4506-89d4-a0227c552f1e"
    # Add more block types as needed


class Blocks:
    def __init__(self, x, y, z, width, height, depth, block_type: BlockType, color="0B9ADE"):
        self.pos = {"x": x, "y": y, "z": z}
        self.bounds = {"x": width, "y": height, "z": depth}
        self.shapeId = block_type.value
        self.color = color
        self.xaxis = 1
        self.zaxis = 3

    def to_dict(self):
        return {
            "bounds": self.bounds,
            "color": self.color,
            "pos": self.pos,
            "shapeId": self.shapeId,
            "xaxis": self.xaxis,
            "zaxis": self.zaxis
        }


class Blueprint:
    def __init__(self):
        self.parts = []
        self._id_counter = 1  # Start IDs at 1

    def add_gate(self, gate: LogicGate):
        gate.id = self._id_counter
        self._id_counter += 1
        self.parts.append(gate)

    def add_gate_matrix(self, width, height, depth, start_x, start_y, start_z, mode: LogicMode, collapse=False):
        """
        Add a 3D matrix of logic gates.
        Returns a 3D list [layer][row][col] of LogicGate objects:
            layer = Z (depth)
            row = Y (height)
            col = X (width)
        """
        matrix = []
        for z in range(depth):
            layer = []
            for y in range(height):
                row = []
                for x in range(width):
                    if collapse:
                        gate = LogicGate(
                            x=start_x,
                            y=start_y,
                            z=start_z,
                            mode=mode
                        )
                    else:
                        gate = LogicGate(
                            x=start_x + x,
                            y=start_y + y,
                            z=start_z + z,
                            mode=mode
                        )
                    self.add_gate(gate)
                    row.append(gate)
                layer.append(row)
            matrix.append(layer)
        return matrix

    def add_block(self, block: Blocks):
        self.parts.append(block)

    def to_json(self):
        body = {
            "childs": [gate.to_dict() for gate in self.parts]
        }
        blueprint = {
            "version": 4,
            "bodies": [body]
        }
        return json.dumps(blueprint, indent=4)
    
    def write(self, filename):
        with open(filename, "w") as f:
            f.write(self.to_json())

__all__ = ['Blueprint', 'LogicGate', 'LogicMode', 'BlockType', 'Blocks']