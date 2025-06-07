import smblueprint as sm
from smblueprint.components import memory, char

bp = sm.Blueprint()

mem = memory(bp, 8, 8)
display = char(bp, "TWN16.bdf",0,0,2)

for i in range(8):
        mem.data_out[i].connect_to(display.input[i])


bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")