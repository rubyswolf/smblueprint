import smblueprint as sm
from smblueprint.components import memory, memory_read, memory_flip, invert

bp = sm.Blueprint()

mem = memory(bp, 8, 8)

target_address = [sm.LogicGate(i, 1, 0, sm.LogicMode.OR) for i in range(mem.address_bits)]
for bit in target_address:
    bp.add(bit)

inverted_address = invert(bp, target_address).output

for i in range(mem.address_bits):
    inverted_address[i].pos["x"]+=i
    inverted_address[i].pos["y"]=2

# mem_flip = memory_flip(bp, mem, target_address, inverted_address)
# for i in range(mem.bits):
#     mem_flip.input[i].pos["x"]+=i
#     mem_flip.input[i].pos["y"]=2

mem_read = memory_read(bp, mem, target_address, inverted_address)
for i in range(mem.bits):
    mem_read.output[i].pos["x"]+=i
    mem_read.output[i].pos["y"]=2

bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")