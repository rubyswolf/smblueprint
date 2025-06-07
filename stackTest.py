import smblueprint as sm
from smblueprint.components import stack

bp = sm.Blueprint()

my_stack = stack(bp, 8, 8, True, True)
for i in range(8):
    my_stack.input[i].pos["x"] = i
    my_stack.input[i].pos["y"] = 1
    my_stack.output[i].pos["x"] = i
    my_stack.output[i].pos["y"] = 2
    my_stack.push.pos["x"] = 1
    my_stack.pop.pos["x"] = 2
    my_stack.gate.pos["x"] = 3

    # Expose the stack's internal memory for debugging
    for j in range(8):
        my_stack.memory.data[j][i].pos["x"] = i
        my_stack.memory.data[j][i].pos["y"] = j+3

bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")