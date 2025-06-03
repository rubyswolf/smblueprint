from PIL import Image

class picture:
    def __init__(self, bp, image, block_type=sm.BlockType.PLASTIC):
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                color_hex = f"{r:02X}{g:02X}{b:02X}"
                bp.add_block(sm.Blocks(x, y, 0, 1, 1, 1, block_type, color_hex))
