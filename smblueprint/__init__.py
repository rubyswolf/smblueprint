import json
from enum import IntEnum, Enum

class Part:
    def __init__(self, x, y, z, color, shapeId, xaxis, zaxis):
        self.id = None
        self.color = color
        self.pos = {"x": x, "y": y, "z": z}
        self.controllers = []
        self.shapeId = shapeId
        self.xaxis = xaxis
        self.zaxis = zaxis

    def connect_to(self, target):
        self.controllers.append({"id": target.id})
        if len(self.controllers) > 256:
            raise ValueError("Part with more than 256 connections")

    def to_dict(self):
        return {
            "color": self.color,
            "controller": {
                "id": self.id,
                "active": False,
                "controllers": self.controllers or None,
                "joints": None
            },
            "pos": self.pos,
            "shapeId": self.shapeId,
            "xaxis": self.xaxis,
            "zaxis": self.zaxis
        }

class LogicMode(IntEnum):
    AND = 0
    OR = 1
    XOR = 2
    NAND = 3
    NOR = 4
    XNOR = 5

class LogicGate(Part):
    def __init__(self, x, y, z, mode: LogicMode, color="DF7F01"):
        super().__init__(x, y, z, color, "9f0f56e8-2c31-4d83-996c-d00a9b296c3f", 2, 1)
        self.mode = mode

    def to_dict(self):
        d = super().to_dict()
        d["controller"]["mode"] = self.mode
        return d

class BlockType(Enum):
    PLASTIC = "628b2d61-5ceb-43e9-8334-a4135566df7a"
    METAL1 = "8aedf6c2-94e1-4506-89d4-a0227c552f1e"
    BARRIER = "09ca2713-28ee-4119-9622-e85490034758"
    # Add more block types as needed

class Timer(Part):
    def __init__(self, x, y, z, delay, color="DF7F01"):
        super().__init__(x, y, z, color, "8f7fd0e7-c46e-4944-a414-7ce2437bb30f", 1, 3)
        self.seconds = delay // 40
        self.ticks = delay % 40

    def to_dict(self):
        d = super().to_dict()
        d["controller"]["seconds"] = self.seconds
        d["controller"]["ticks"] = self.ticks
        return d

class Switch(Part):
    def __init__(self, x, y, z, color="DF7F01"):
        super().__init__(x, y, z, color, "7cf717d7-d167-4f2d-a6e7-6b2c70aa3986", 2, 1)

class Button(Part):
    def __init__(self, x, y, z, color="DF7F01"):
        super().__init__(x, y, z, color, "1e8d93a4-506b-470d-9ada-9c0a321e2db5", 2, 1)

class Toilet(Part):
    def __init__(self, x, y, z, color="3E9FFE"):
        super().__init__(x, y, z, color, "ca003562-fde7-463c-969e-f8334ae54387", -1, 2)

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
        if hasattr(part, 'id'):
            part.id = self._id_counter
            self._id_counter += 1
        self.parts.append(part)

    def merge(self, target, source):
        target_ids = {c["id"] for c in getattr(target, "controllers", [])}
        for c in getattr(source, "controllers", []):
            if c["id"] not in target_ids:
                getattr(target, "controllers", []).append({"id": c["id"]})
                target_ids.add(c["id"])
        for part in self.parts:
            if hasattr(part, "controllers"):
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