import smblueprint as sm
from smblueprint.components import memory, char

addresses = 16
bits = 8
program_size = 8

mem = memory(sm.Blueprint(), addresses, bits)

bp = sm.Blueprint()
