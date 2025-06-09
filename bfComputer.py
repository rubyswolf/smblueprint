import smblueprint as sm
from smblueprint.components import stack, char, invert, rom, memory, memory_read, memory_write, memory_increment, memory_decrement, memory_set, equals, rising_edge
import math

script = "every_second.bf" # Program for the computer to run

# Computer configuration

bits = 8 # Global number of bits
memory_size = 16 # Number of addresses in the memory

#IO
# Note the if the size of the input buffer is a power of two then the stack pointer may wrap around and the input "abcd" will be seen as "abcdabcdabcd..." continually
input_size = 6 # Size of the input buffer
output_size = 6 # Size of the output buffer

reset_button = True # Whether to add a reset button to the computer

memory_address_size = math.ceil(math.log2(memory_size)) # Number of bits needed to address the memory

# Read the script file
with open("scripts/"+script, 'r') as file:
    program = file.read()

# Strip all characters that aren't <>+-.,[]
program = ''.join(filter(lambda x: x in '<>+-.,[]', program))

# Make sure all brackets match
if program.count('[') != program.count(']'):
    raise ValueError("Unmatched brackets in the script")

# Make sure a closing bracket doesn't occur first
if program.find(']') < program.find('['):
    raise ValueError("Closing bracket before opening bracket in the script")

program_length = len(program)
program_address_size = math.ceil(math.log2(program_length)) # Number of bits needed to address the program

# < = 0
# > = 1
# + = 2
# - = 3
# . = 4
# , = 5
# [ = 6
# ] = 7

# Convert the program into a list of integers
# Final value is 6, which will be used to halt the computer
program_data = [0] * program_length
for i, program_char in enumerate(program):
    if program_char == '<':
        program_data[i] = 0
    elif program_char == '>':
        program_data[i] = 1
    elif program_char == '+':
        program_data[i] = 2
    elif program_char == '-':
        program_data[i] = 3
    elif program_char == '.':
        program_data[i] = 4
    elif program_char == ',':
        program_data[i] = 5
    elif program_char == '[':
        program_data[i] = 6
    elif program_char == ']':
        program_data[i] = 7

# Create the data structure for the correct location to jump to when encountering each bracket
bracket_data = {}
for i in range(program_length):
    if program[i] == '[':
        counter = 0
        for j in range(i+1, program_length):
            if program[j] == '[':
                counter += 1
            if program[j] == ']':
                if counter == 0: # Found the matching closing bracket
                    bracket_data[i] = j+1 # Jump to after the closing bracket
                    bracket_data[j] = i+1 # Jump to after the opening bracket
                    break
                else:
                    counter -= 1

print("Program read")

halt_constant = 2**(program_address_size+1)-1 # Halt instruction, sets the halt bit to 1

# Add the halt instruction
bracket_data[program_length] = halt_constant # Halt instruction, will be used to stop the computer once it reaches the end of the program

# print(program_data)
# print(bracket_data)
# exit()

bp = sm.Blueprint()

constant_low = sm.LogicGate(0, 0, 0, sm.LogicMode.OR, "00FF00")
bp.add(constant_low)
constant_high = sm.LogicGate(0, 0, 0, sm.LogicMode.NOR, "FF0000")
bp.add(constant_high)
constant_low.connect_to(constant_high)

# Running State
halted = memory(bp, 1, 1)  # Memory to indicate if the computer is halted
halted_value = halted.data[0][0]  # The actual halted value
halted_value.color = "FF0000"  # Color the halted value red
halted_value.pos["x"] = -3
not_halted = sm.LogicGate(0, 0, 0, sm.LogicMode.NOR, "FF0000")  # Logic gate to indicate if the computer is not halted
bp.add(not_halted)
halted_value.connect_to(not_halted)

running = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)  # Logic gate to indicate if the computer is running
bp.add(running)
not_halted.connect_to(running)

enable = sm.LogicGate(-1, 0, 0, sm.LogicMode.AND, "00FF00")  # Logic gate to enable the computer
bp.add(enable)
enable.connect_to(running)

tick = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)  # Logic gate to indicate a tick
bp.add(tick)
running.connect_to(tick)

trigger_tick = sm.LogicGate(-2, 0, 0, sm.LogicMode.OR, "FFFF00") # Logic gate to trigger the tick
bp.add(trigger_tick)
trigger_tick.connect_to(tick)  # Connect the trigger tick to the tick logic gate

# PC
program_counter = memory(bp, 1, program_address_size)  # Memory for the program counter
program_counter_value = program_counter.data[0]  # The actual program counter value
program_counter_value_inverted = invert(bp, program_counter_value).output  # Inverted program counter for reading

for i in range(program_address_size):
    program_counter_value[i].color = "00FF00"  # Color the program counter value green
    program_counter_value[i].pos["x"] = i+4  # Position the program counter value
    program_counter_value[i].pos["y"] = -1

# Program counter operations
program_counter_write = memory_write(bp, program_counter, 1)  # Write operation for the program counter
program_counter_increment = memory_increment(bp, program_counter, True, 1)  # Increment operation for the program counter

bp.merge(enable, program_counter_increment.gate)

# ROMs
program_rom = rom(bp, program_counter_value, program_counter_value_inverted, 3, program_data)  # ROM for the program
bracket_data_rom = rom(bp, program_counter_value, program_counter_value_inverted, program_address_size+1, bracket_data)  # ROM for the bracket data

for i in range(len(program_rom.output)):
    program_rom.output[i].color = "000000"
    program_rom.output[i].pos["x"] = i+8
    program_rom.output[i].pos["y"] = 1

for i in range(len(bracket_data_rom.output)):
    bracket_data_rom.output[i].color = "00FFFF"
    bracket_data_rom.output[i].pos["x"] = i+8

# Memory for the computer
mem = memory(bp, memory_size, bits)  # Main memory for the computer

for i in range(memory_size):
    for j in range(bits):
        mem.data[i][j].pos["x"] = i-memory_size-1
        mem.data[i][j].pos["y"] = j+2
        mem.data[i][j].pos["z"] = 1

bp.add(sm.Blocks(-1, 2, 1, 1, bits, 1, sm.BlockType.PLASTIC, "000000"))

# Memory pointer
mem_pointer = memory(bp, 1, memory_address_size)  # Memory for the current memory address
mem_pointer_value = mem_pointer.data[0]  # The actual memory address value
mem_pointer_value_inverted = invert(bp, mem_pointer_value).output  # Inverted memory address for reading

for i in range(memory_address_size):
    mem_pointer_value[i].color = "FFFF00"
    mem_pointer_value[i].pos["x"] = i+4
    mem_pointer_value[i].pos["y"] = 0

# Memory pointer operations
mem_pointer_write = memory_write(bp, mem_pointer, 0)  # Write operation for the memory pointer
mem_pointer_increment = memory_increment(bp, mem_pointer, True, 0)  # Increment operation for the memory pointer
mem_pointer_decrement = memory_decrement(bp, mem_pointer, True, 0)  # Decrement operation for the memory pointer
bp.merge(enable, mem_pointer_increment.gate)
bp.merge(enable, mem_pointer_decrement.gate)

# Memory operations
mem_read = memory_read(bp, mem, mem_pointer_value, mem_pointer_value_inverted)  # Read operation for the memory
mem_write = memory_write(bp, mem, mem_pointer_value, mem_pointer_value_inverted)  # Write operation for the memory
mem_increment = memory_increment(bp, mem, True, mem_pointer_value, mem_pointer_value_inverted)  # Increment operation for the memory pointer
mem_decrement = memory_decrement(bp, mem, True, mem_pointer_value, mem_pointer_value_inverted)  # Decrement operation for the memory pointer

bp.merge(enable, mem_increment.gate)
bp.merge(enable, mem_decrement.gate)

# Input buffer
input_buffer = stack(bp, input_size, bits, True, True)
bp.merge(constant_high, input_buffer.gate)

# Player controls
bp.add(sm.Blocks(3, -3, 0, 1, 4, 1, sm.BlockType.PLASTIC, "000000"))
bp.add(sm.Blocks(-2, 1, 0, 2, 1, 1, sm.BlockType.PLASTIC, "000000"))

enable_switch = sm.Switch(-1, 1, 1, "00FF00")  # Switch to enable the computer
bp.add(enable_switch)
enable_switch.connect_to(enable)  # Connect the enable switch to the enable logic gate

tick_button = sm.Button(-2, 1, 1, "FFFF00")  # Button to trigger a tick
bp.add(tick_button)
external_tick = rising_edge(bp, tick_button) # Create a rising edge from the button press to trigger the tick logic gate
external_tick.output.connect_to(trigger_tick)  # Connect the external tick to the trigger tick logic gate

main_toilet = sm.Toilet(5,-4, 1)
bp.add(main_toilet)  # Add the toilet to the blueprint


for i in range(bits):
    input_buffer.input[i].pos["x"] = i
    input_buffer.input[i].pos["y"] = 1

    bit_switch = sm.Switch(i, 1, 1, "FFFFFF")
    bp.add(bit_switch)
    bit_switch.connect_to(input_buffer.input[i])  # Connect the switch to the input buffer pointer bit
    main_toilet.connect_to(bit_switch)  # Connect the toilet to the switch

for i in range(input_buffer.pointer.bits):
    input_buffer.pointer.data[0][i].color = "FFFFFF"
    input_buffer.pointer.data[0][i].pos["x"] = i+8+len(program_rom.output)
    input_buffer.pointer.data[0][i].pos["y"] = 1


bp.add(sm.Blocks(1, 0, 0, 2, 1, 1, sm.BlockType.PLASTIC, "000000"))

push_button = sm.Button(1, 0, 1, "00FF00")  # Button to push data into the input buffer
bp.add(push_button)
rising_edge(bp, push_button).output.connect_to(input_buffer.push)  # Connect the button press to the input buffer push operation
pop_button = sm.Button(2, 0, 1, "FF00FF")  # Button to pop data from the input buffer
bp.add(pop_button)
rising_edge(bp, pop_button).output.connect_to(input_buffer.pop)  # Connect the button press to the input buffer pop operation

main_toilet.connect_to(push_button)  # Connect the toilet to the push button
main_toilet.connect_to(pop_button)  # Connect the toilet to the pop button

# accessible_push = sm.LogicGate(1, 0, 0, sm.LogicMode.AND, "00FF00")
# bp.add(accessible_push)
# accessible_push.connect_to(input_buffer.push)
# accessible_pop = sm.LogicGate(2, 0, 0, sm.LogicMode.AND, "FF00FF")
# bp.add(accessible_pop)
# accessible_pop.connect_to(input_buffer.pop)



input_pointer = memory(bp, 1, input_buffer.pointer.bits) # Pointer for reading the input buffer
input_pointer_value = input_pointer.data[0]  # The actual input pointer value
input_pointer_value_inverted = invert(bp, input_pointer_value).output  # Inverted input pointer for reading

input_pointer_increment = memory_increment(bp, input_pointer, False, 0)

input_read = memory_read(bp, input_buffer.memory, input_pointer_value, input_pointer_value_inverted)  # Read operation for the input buffer

# Output buffer
output_buffer = stack(bp, output_size, bits, True, True)
bp.merge(constant_high, output_buffer.gate)
constant_low.connect_to(output_buffer.pop)

for i in range(output_buffer.pointer.bits):
    output_buffer.pointer.data[0][i].color = "000000"
    output_buffer.pointer.data[0][i].pos["x"] = i+8+len(program_rom.output)+input_buffer.pointer.bits
    output_buffer.pointer.data[0][i].pos["y"] = 1

# set_output_pointer_max = memory_set(bp, output_buffer.pointer, 0, 2**(output_buffer.pointer.bits+1)-1)
# inital_pulse = rising_edge(bp, constant_high).output  # Initial pulse to set the output pointer to the maximum value
# inital_pulse.connect_to(set_output_pointer_max.trigger)  # Connect the initial pulse to the set output pointer operation
# rising_edge(bp, enable).output.connect_to(memory_set(bp, output_buffer.pointer, 0, 2**(output_buffer.pointer.bits+1)-1).trigger)  # Set the output pointer to the maximum value when the computer is enabled

print("Created data structures")

input_memory_inverted = [invert(bp, input_buffer.memory.data[i]).output for i in range(input_size)]
output_memory_inverted = [invert(bp, output_buffer.memory.data[i]).output for i in range(output_size)]

# Supporting blocks
bp.add(sm.Blocks(0,18,1,max(input_size, output_size)*8,1,1,sm.BlockType.PLASTIC, "000000"))
bp.add(sm.Blocks(0,2,0,1,1,1,sm.BlockType.PLASTIC, "000000"))

# Displays
input_display = [char(bp, "TWN16.bdf", input_buffer.memory.data[i], input_memory_inverted[i], 8*i, 19, 1) for i in range(input_size)]
output_display = [char(bp, "TWN16.bdf", output_buffer.memory.data[i], output_memory_inverted[i], 8*i, 2, 1) for i in range(output_size)]

print("Created displays")

# Logic for the computer
program_rom_inverted = invert(bp, program_rom.output).output # Inverted output of the program ROM

if_move_left = equals(bp, program_rom.output, 0, program_rom_inverted).output # <
if_move_right = equals(bp, program_rom.output, 1, program_rom_inverted).output # >
if_increment = equals(bp, program_rom.output, 2, program_rom_inverted).output # +
if_decrement = equals(bp, program_rom.output, 3, program_rom_inverted).output # -
if_output = equals(bp, program_rom.output, 4, program_rom_inverted).output # .
if_input = equals(bp, program_rom.output, 5, program_rom_inverted).output # ,
if_while_start_jump = equals(bp, program_rom.output, 6, program_rom_inverted).output # [ (command run)
if_while_start_skip = equals(bp, program_rom.output, 6, program_rom_inverted).output # [ (command ignored)
if_while_end_jump = equals(bp, program_rom.output, 7, program_rom_inverted).output # ] (command run)
if_while_end_skip = equals(bp, program_rom.output, 7, program_rom_inverted).output # ] (command ignored)

trigger_move_left = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_move_right = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_increment = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_decrement = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_output = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_input = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_while_start_jump = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_while_start_skip = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_while_end_jump = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)
trigger_while_end_skip = sm.LogicGate(0, 0, 0, sm.LogicMode.AND)

bp.add(trigger_move_left)
bp.add(trigger_move_right)
bp.add(trigger_increment)
bp.add(trigger_decrement)
bp.add(trigger_output)
bp.add(trigger_input)
bp.add(trigger_while_start_jump)
bp.add(trigger_while_start_skip)
bp.add(trigger_while_end_jump)
bp.add(trigger_while_end_skip)

if_move_left.connect_to(trigger_move_left)
if_move_right.connect_to(trigger_move_right)
if_increment.connect_to(trigger_increment)
if_decrement.connect_to(trigger_decrement)
if_output.connect_to(trigger_output)
if_input.connect_to(trigger_input)
if_while_start_jump.connect_to(trigger_while_start_jump)
if_while_start_skip.connect_to(trigger_while_start_skip)
if_while_end_jump.connect_to(trigger_while_end_jump)
if_while_end_skip.connect_to(trigger_while_end_skip)

tick.connect_to(trigger_move_left)
tick.connect_to(trigger_move_right)
tick.connect_to(trigger_increment)
tick.connect_to(trigger_decrement)
tick.connect_to(trigger_output)
tick.connect_to(trigger_input)
tick.connect_to(trigger_while_start_jump)
tick.connect_to(trigger_while_start_skip)
tick.connect_to(trigger_while_end_jump)
tick.connect_to(trigger_while_end_skip)

non_jumping_command = sm.LogicGate(0, 0, 0, sm.LogicMode.NOR)  # Logic gate to check if the command is not a jumping command
bp.add(non_jumping_command)
if_while_start_jump.connect_to(non_jumping_command)  # Connect the while start command to the non-jumping command
if_while_end_jump.connect_to(non_jumping_command)  # Connect the while end command to the non-jumping command

# Increment the program counter
program_counter_increment.trigger.mode = sm.LogicMode.AND  # Set the program counter increment trigger to AND mode so it only triggers when the command is not a jumping command and the tick occurs
non_jumping_command.connect_to(program_counter_increment.trigger)  # Connect the non-jumping command to the increment program counter trigger
tick.connect_to(program_counter_increment.trigger)  # Connect the tick to the increment program counter trigger

# Move left
trigger_move_left.connect_to(mem_pointer_decrement.trigger)  # Decrement the memory pointer

# Move right
trigger_move_right.connect_to(mem_pointer_increment.trigger)  # Increment the memory pointer

# Increment memory
trigger_increment.connect_to(mem_increment.trigger)  # Increment the memory at the current pointer

# Decrement memory
trigger_decrement.connect_to(mem_decrement.trigger)  # Decrement the memory at the current pointer


# Output to the output buffer
for i in range(bits):
    mem_read.output[i].connect_to(output_buffer.input[i])  # Read the memory at the current pointer and output to the output buffer

trigger_output.connect_to(output_buffer.push)  # Push the output buffer

# Input from the input buffer
for i in range(bits):
    input_read.output[i].connect_to(mem_write.input[i])  # Read the input buffer and write to the memory at the current pointer

trigger_input.connect_to(mem_write.trigger)  # Trigger the memory write operation
trigger_input.connect_to(input_pointer_increment.trigger)  # Increment the input pointer after reading

# While loop common
for i in range(program_address_size):
    bracket_data_rom.output[i].connect_to(program_counter_write.input[i])  # Prepare to write the location to jump to when encountering a bracket to the program counter

zero_memory = sm.LogicGate(0, 0, 0, sm.LogicMode.NOR)  # Logic gate to check if the memory at the current pointer is zero
bp.add(zero_memory)
nonzero_memory = sm.LogicGate(0, 0, 0, sm.LogicMode.OR)  # Logic gate to check if the memory at the current pointer is non-zero
bp.add(nonzero_memory)

# While loop start
for i in range(bits):
    mem_read.output[i].connect_to(zero_memory)  # Connect the memory read output to the zero check

zero_memory.connect_to(if_while_start_jump)  # Connect the zero check to the while start
nonzero_memory.connect_to(if_while_start_skip)

trigger_while_start_jump.connect_to(program_counter_write.trigger)  # Write the location to jump to when encountering a while start bracket to the program counter

# While loop end
for i in range(bits):
    mem_read.output[i].connect_to(nonzero_memory)  # Connect the memory read output to the non-zero check

nonzero_memory.connect_to(if_while_end_jump)  # Connect the non-zero check to the while end
zero_memory.connect_to(if_while_end_skip)

trigger_while_end_jump.connect_to(program_counter_write.trigger)  # Write the location to jump to when encountering a while end bracket to the program counter

# Halt
rising_edge(bp, bracket_data_rom.output[-1]).output.connect_to(halted_value)  # Connect the halt trigger to the halted value

# Run continuously

# Old clock based approach
# cycle_delay = sm.Timer(0, 0, 0, 8)  # Timer to create a cycle delay
# bp.add(cycle_delay)

# tick.connect_to(cycle_delay)  # Connect the tick to the cycle delay
# cycle_delay.connect_to(trigger_tick)  # Connect the cycle delay output to the tick trigger

# Dynamic cycles

# Increment and Decrement
increment_delay = sm.Timer(0, 0, 0, 6)
bp.add(increment_delay)
trigger_increment.connect_to(increment_delay)
increment_delay.connect_to(trigger_tick)

decrement_delay = sm.Timer(0, 0, 0, 6)
bp.add(decrement_delay)
trigger_decrement.connect_to(decrement_delay)
decrement_delay.connect_to(trigger_tick)

# Left and Right
move_left_delay = sm.Timer(0, 0, 0, 7)
bp.add(move_left_delay)
trigger_move_left.connect_to(move_left_delay)
move_left_delay.connect_to(trigger_tick)

move_right_delay = sm.Timer(0, 0, 0, 7)
bp.add(move_right_delay)
trigger_move_right.connect_to(move_right_delay)
move_right_delay.connect_to(trigger_tick)

# Input and Output
input_delay = sm.Timer(0, 0, 0, 5)
bp.add(input_delay)
trigger_input.connect_to(input_delay)
input_delay.connect_to(trigger_tick)

output_delay = sm.Timer(0, 0, 0, 5)
bp.add(output_delay)
trigger_output.connect_to(output_delay)
output_delay.connect_to(trigger_tick)

# Jumping While
while_start_jump_delay = sm.Timer(0, 0, 0, 5)
bp.add(while_start_jump_delay)
trigger_while_start_jump.connect_to(while_start_jump_delay)
while_start_jump_delay.connect_to(trigger_tick)

while_end_jump_delay = sm.Timer(0, 0, 0, 5)
bp.add(while_end_jump_delay)
trigger_while_end_jump.connect_to(while_end_jump_delay)
while_end_jump_delay.connect_to(trigger_tick)

# Skipping While
while_start_skip_delay = sm.Timer(0, 0, 0, 5)
bp.add(while_start_skip_delay)
trigger_while_start_skip.connect_to(while_start_skip_delay)
while_start_skip_delay.connect_to(trigger_tick)

while_end_skip_delay = sm.Timer(0, 0, 0, 5)
bp.add(while_end_skip_delay)
trigger_while_end_skip.connect_to(while_end_skip_delay)
while_end_skip_delay.connect_to(trigger_tick)



if reset_button:
    bp.add(sm.Blocks(-4, 0, 0, 1, 1, 1, sm.BlockType.BARRIER, "CE9E0C"))
    reset_button = sm.Button(-5, 0, 1, "FF0000")  # Reset button to reset the computer
    bp.add(reset_button)

    reset_trigger = rising_edge(bp, reset_button, -5, 0, 0).output  # Create a rising edge from the reset button press
    for i in range(memory_size):
        reset_trigger.connect_to(memory_set(bp, mem, i, 0, None, -5, 0, 0).trigger)  # Reset the memory to zero

    reset_trigger.connect_to(memory_set(bp, halted, 0, 0, None, -5, 0, 0).trigger)  # Reset the halted state to zero
    reset_trigger.connect_to(memory_set(bp, program_counter, 0, 0, None, -5, 0, 0).trigger)  # Reset the program counter to zero
    reset_trigger.connect_to(memory_set(bp, mem_pointer, 0, 0, None, -5, 0, 0).trigger)  # Reset the memory pointer to zero
    reset_trigger.connect_to(memory_set(bp, input_pointer, 0, 0, None, -5, 0, 0).trigger)  # Reset the input pointer to zero
    reset_trigger.connect_to(memory_set(bp, output_buffer.pointer, 0, 2**(output_buffer.pointer.bits)-1, None, -5, 0, 0).trigger)  # Reset the output pointer to the maximum value

    # Clear the output buffer
    for i in range(output_size):
        reset_trigger.connect_to(memory_set(bp, output_buffer.memory, i, 0, None, -5, 0, 0).trigger)  # Reset the output buffer memory to zero

print("Created Computer logic")

# bp.write("C:\\Users\\TechFast Australia\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198072296012\\Blueprints\\33a4d966-7df2-42ff-b0b4-eb0cafcadeca\\blueprint.json")
bp.write("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\blueprint.json")

print("Blueprint written to file")