import smblueprint as sm
from smblueprint.components import memory, memory_read, memory_flip, invert, memory_increment, memory_decrement, memory_write, memory_set

bp = sm.Blueprint()

mem = memory(bp, 8, 8)

target_address = [sm.LogicGate(i, 1, 0, sm.LogicMode.OR) for i in range(mem.address_bits)]
for bit in target_address:
    bp.add(bit)

inverted_address = invert(bp, target_address).output

mem_flip = memory_flip(bp, mem, target_address, inverted_address)
for i in range(mem.bits):
    mem_flip.input[i].pos["x"]+=i
    mem_flip.input[i].pos["y"]=3

mem_read = memory_read(bp, mem, target_address, inverted_address)
for i in range(mem.bits):
    mem_read.output[i].pos["x"]+=i
    mem_read.output[i].pos["y"]=4

mem_inc = memory_increment(bp, mem, True, target_address, inverted_address)
mem_inc.trigger.pos["x"] = 3
mem_inc.trigger.pos["y"] = 1
mem_inc.gate.pos["x"] = 4
mem_inc.gate.pos["y"] = 1

mem_dec = memory_decrement(bp, mem, True, target_address, inverted_address)
mem_dec.trigger.pos["x"] = 5
mem_dec.trigger.pos["y"] = 1
mem_dec.gate.pos["x"] = 6
mem_dec.gate.pos["y"] = 1

bp.merge(mem_inc.gate, mem_dec.gate)

mem_write = memory_write(bp, mem, target_address, inverted_address)
for i in range(mem.bits):
    mem_write.input[i].pos["x"]+=i
    mem_write.input[i].pos["y"]=2
mem_write.trigger.pos["x"] = 6
mem_write.trigger.pos["y"] = 1

mem_set = memory_set(bp, mem, target_address, 10, inverted_address)
mem_set.trigger.pos["x"] = 7
mem_set.trigger.pos["y"] = 1

bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")