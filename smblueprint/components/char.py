import smblueprint as sm
from .equals import equals

class char:
    """
    A class to handle character display using a bitmap font.
    Reads a BDF (Bitmap Distribution Format) file and creates a display
    """
    def __init__(self, bp, filepath, input, inverted_input, screen_x=0, screen_y=0, screen_z=0, logic_x=0, logic_y=0, logic_z=0):
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

        self.display = [[sm.LogicGate(screen_x + i, screen_y + j, screen_z, sm.LogicMode.OR) for i in range(8)] for j in range(16)]

        for row in self.display:
            for gate in row:
                bp.add(gate)
        
        decoder = {}

        for char_code in range(256):
            if char_code not in glyphs:
                continue

            bitmap = glyphs[char_code]

            if len(bitmap) != 16:
                print(f"Skipping malformed glyph for char code {char_code}: expected 16 rows, got {len(bitmap)}")
                continue  # Skip malformed glyphs

            decoder[char_code] = equals(bp, input, char_code, inverted_input, logic_x, logic_y, logic_z).output

            for y in range(16):
                row = bitmap[y]
                for x in range(8):
                    if (row >> x) & 1:
                        decoder[char_code].connect_to(self.display[15-y][7-x])