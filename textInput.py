import smblueprint as sm
from smblueprint.components import stack, char, invert

bp = sm.Blueprint()

size = 8

my_stack = stack(bp, size, 8, True)
for i in range(8):
    my_stack.input[i].pos["x"] = i
    my_stack.input[i].pos["y"] = 1
    my_stack.output[i].pos["x"] = i
    my_stack.output[i].pos["y"] = 2
    my_stack.push.pos["x"] = 1
    my_stack.pop.pos["x"] = 2
    my_stack.gate.pos["x"] = 3

memory_inverted = [invert(bp, my_stack.memory.data[i]).output for i in range(size)]

displays = [char(bp, "TWN16.bdf", my_stack.memory.data[(i+1)%size], memory_inverted[(i+1)%size], 8*i, 3, 0) for i in range(size)]

bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")