from datetime import timedelta

# === Configuration ===
FILENAME = "every_second.bf"  # File containing Brainfuck code
bf_input = "00000"            # Hardcoded Brainfuck input string

# === Load Brainfuck Code from File ===
with open("./scripts/"+FILENAME, "r") as f:
    bf_code = f.read()

# === Brainfuck Interpreter ===
def run_brainfuck(code, bf_input):
    tape = [0] * 30000
    ptr = 0
    input_ptr = 0
    output = ""
    steps = 0
    max_ptr = 0

    # Preprocess bracket matching
    bracket_map = {}
    stack = []
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start

    i = 0
    while i < len(code):
        c = code[i]
        steps += 1

        if c == ">":
            ptr += 1
            if ptr >= len(tape):
                tape.append(0)
        elif c == "<":
            ptr -= 1
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) % 256
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) % 256
        elif c == ".":
            output += chr(tape[ptr])
        elif c == ",":
            if input_ptr < len(bf_input):
                tape[ptr] = ord(bf_input[input_ptr])
                input_ptr += 1
            else:
                tape[ptr] = 0
        elif c == "[":
            if tape[ptr] == 0:
                i = bracket_map[i]
        elif c == "]":
            if tape[ptr] != 0:
                i = bracket_map[i]

        max_ptr = max(max_ptr, ptr)
        i += 1

    return output, steps, (max_ptr + 1)

# === Time formatting ===
def format_timecode(seconds):
    return str(timedelta(seconds=round(seconds)))

# === Run and Report ===
output, steps, memory_used = run_brainfuck(bf_code, bf_input)
base_runtime_timecode = format_timecode(steps / 4)
fast_runtime_timecode = format_timecode(steps / (4*256))  # Assuming 256x speedup


print("Program Output:")
print(output)
print("\n--- Stats ---")
print(f"Input length: {len(bf_input)}")
print(f"Output length: {len(output)}")
print(f"Steps executed: {steps}")
print(f"Estimated runtime at vanilla speed (4 steps/sec): {base_runtime_timecode}")
print(f"Estimated runtime at fast speed (256x speed): {fast_runtime_timecode}")
print(f"Memory used (cells accessed): {memory_used}")
