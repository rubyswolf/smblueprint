import smblueprint as sm
from smblueprint.components import rom, invert

bp = sm.Blueprint()

input_addr = [sm.LogicGate(i, 1, 0, sm.LogicMode.OR) for i in range(3)]
for bit in input_addr:
    bp.add(bit)

inverted_addr = invert(bp, input_addr).output

test_rom = rom(bp,input_addr,inverted_addr, 8, {1: 10, 5: 20})

for i in range(8):
        test_rom.output[i].pos["x"] = i
        test_rom.output[i].pos["y"] = 2

bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")