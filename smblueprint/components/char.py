import smblueprint as sm
from .decoder import decoder

class char:
    def __init__(self, bp, filepath, x=0, y=0, z=0):
        dec = decoder(bp, 8, x, y, z)
        self.input = dec.input
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

        display = [[sm.LogicGate(x + i, y + j, z+1, sm.LogicMode.OR) for i in range(8)] for j in range(16)]

        for row in display:
            for gate in row:
                bp.add_gate(gate)

        for char_code in range(256):
            if char_code not in glyphs:
                continue

            bitmap = glyphs[char_code]

            if len(bitmap) != 16:
                print(f"Skipping malformed glyph for char code {char_code}: expected 16 rows, got {len(bitmap)}")
                continue  # Skip malformed glyphs

            for y in range(16):
                row = bitmap[y]
                for x in range(8):
                    if (row >> x) & 1:
                        dec.output[char_code].connect_to(display[y][x])