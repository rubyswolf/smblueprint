import smblueprint as sm
from smblueprint.components import invert, equals

bp = sm.Blueprint()

input_array = [sm.LogicGate(i, 0, 0, sm.LogicMode.OR) for i in range(8)]
for bit in input_array:
    bp.add(bit)

inverted_input = invert(bp, input_array).output
for i in range(8):
    inverted_input[i].pos["z"] = 1
    inverted_input[i].pos["x"] = i

equals_decoder = [equals(bp,input_array,i,inverted_input).output for i in range(256)]
for i in range(256):
    equals_decoder[i].pos["x"] = i
    equals_decoder[i].pos["y"] = 1

bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")