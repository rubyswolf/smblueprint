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
        self.id = None
        self.mode = mode
        self.color = color
        self.pos = {"x": x, "y": y, "z": z}
        self.controllers = []
        self.shapeId = "9f0f56e8-2c31-4d83-996c-d00a9b296c3f"
        self.xaxis = 2
        self.zaxis = 1

    def connect_to(self, target):
        self.controllers.append({"id": target.id})

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

class Timer:
    def __init__(self, x, y, z, delay, color="DF7F01"):
        self.id = None
        self.pos = {"x": x, "y": y, "z": z}
        self.color = color
        self.controllers = []
        self.seconds = delay//40
        self.ticks = delay%40
        self.shapeId = "8f7fd0e7-c46e-4944-a414-7ce2437bb30f"  # Replace with actual shape ID
        self.xaxis = 1
        self.zaxis = 3

    def connect_to(self, target):
        self.controllers.append({"id": target.id})

    def to_dict(self):
        return {
            "color": self.color,
            "controller": {
                "id": self.id,
                "active": False,
                "controllers": self.controllers or None,
                "joints": None,
                "seconds": self.seconds,
                "ticks": self.ticks
            },
            "pos": self.pos,
            "shapeId": self.shapeId,
            "xaxis": self.xaxis,
            "zaxis": self.zaxis
        }

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

    def add(self, part):
        # Assign an ID if the part has an 'id' attribute (LogicGate or Timer)
        if hasattr(part, 'id'):
            part.id = self._id_counter
            self._id_counter += 1
        self.parts.append(part)

    def merge(self, target, source):
        # Merge controllers from source to target, avoiding duplicates
        target_ids = {c["id"] for c in getattr(target, "controllers", [])}
        for c in getattr(source, "controllers", []):
            if c["id"] not in target_ids:
                getattr(target, "controllers", []).append({"id": c["id"]})
                target_ids.add(c["id"])

        # Update all parts that have source.id as a controller to use target.id, avoiding duplicates
        for part in self.parts:
            if hasattr(part, "controllers"):
                # Remove duplicates after replacement
                new_controllers = []
                seen = set()
                for ctrl in part.controllers:
                    ctrl_id = ctrl["id"]
                    if ctrl_id == source.id:
                        ctrl_id = target.id
                    if ctrl_id not in seen:
                        new_controllers.append({"id": ctrl_id})
                        seen.add(ctrl_id)
                part.controllers = new_controllers

        # Remove the source part from the blueprint
        self.parts = [p for p in self.parts if p is not source]

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

__all__ = ['Blueprint', 'LogicGate', 'LogicMode', 'Timer', 'BlockType', 'Blocks']