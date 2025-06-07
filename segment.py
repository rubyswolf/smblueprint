import smblueprint as sm

bp = sm.Blueprint()

# Stage 1: OR gates (8x1x1) at (0, 0, 0)
or_matrix = bp.add_gate_matrix(8, 1, 1, 0, 0, 0, sm.LogicMode.OR)
ors = or_matrix[0][0]

# Stage 2: NOR gates (8x1x1) directly above ORs at (0, 1, 0)
nor_matrix = bp.add_gate_matrix(8, 1, 1, 0, 1, 0, sm.LogicMode.NOR, collapse=True)
nors = nor_matrix[0][0]

# Connect ORs to corresponding NORs
for i in range(8):
    ors[i].connect_to(nors[i])

# Stage 3: 16x16 AND gate matrix (256 total gates) at (0, 2, 0)
and_matrix = bp.add_gate_matrix(16, 16, 1, 0, 1, 0, sm.LogicMode.AND, collapse=True)
and_gates_flat = [gate for row in and_matrix[0] for gate in row]

# Connect each AND gate to a unique 8-bit combination of OR/NORs
for idx, and_gate in enumerate(and_gates_flat):
    for bit in range(8):
        if (idx >> bit) & 1:
            ors[bit].connect_to(and_gate)
        else:
            nors[bit].connect_to(and_gate)

# Load font from BDF
def parse_bdf_bitmap(filepath):
    glyphs = {}
    with open(filepath, "r") as f:
        lines = f.readlines()

    code = None
    bitmap = []
    recording = False

    for line in lines:
        line = line.strip()

        if line.startswith("STARTCHAR"):
            bitmap = []

        elif line.startswith("ENCODING"):
            code = int(line.split()[1])

        elif line == "BITMAP":
            recording = True

        elif line == "ENDCHAR":
            if code is not None:
                # Pad to 16 rows if needed
                while len(bitmap) < 16:
                    bitmap.insert(0, "00")  # Add blank row at the top
                bitmap = bitmap[:16]  # Truncate if too long
                glyphs[code] = [int(row, 16) for row in bitmap]
            recording = False
            code = None

        elif recording:
            bitmap.append(line)

    return glyphs


font_data = parse_bdf_bitmap("VGA_8x16.bdf")

display_matrix = bp.add_gate_matrix(8, 16, 1, 0, 0, 1, sm.LogicMode.OR)
display_layer = display_matrix[0]

# Connect each AND gate (for character c) to ON pixels in font_data[c]
for char_code in range(256):
    if char_code not in font_data:
        continue  # Skip missing glyphs

    bitmap = font_data[char_code]
    if len(bitmap) != 16:
        print(f"Skipping malformed glyph for char code {char_code}: expected 16 rows, got {len(bitmap)}")
        continue  # Skip malformed glyphs

    and_gate = and_gates_flat[char_code]

    for y in range(16):
        row = bitmap[y]
        for x in range(8):
            if (row >> (7 - x)) & 1:
                and_gate.connect_to(display_layer[y][7-x])

# Export to blueprint.json
with open("blueprint.json", "w") as f:
    f.write(bp.to_json())
