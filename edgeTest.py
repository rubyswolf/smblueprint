import smblueprint as sm
from smblueprint.components import rising_edge, falling_edge, dual_edge

bp = sm.Blueprint()

input = sm.LogicGate(0, 0, 0, sm.LogicMode.OR)
bp.add(input)

rise = rising_edge(bp, input, 0, 1, 0).output
rise.pos["y"] = 2

fall = falling_edge(bp, input, 0, 1, 0).output
fall.pos["y"] = 3

dual = dual_edge(bp, input, 0, 1, 0).output
dual.pos["y"] = 4

bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")