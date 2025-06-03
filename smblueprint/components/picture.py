from PIL import Image
import smblueprint as sm

class picture:
    """
    Represents a picture component that can be added to a Scrap Mechanic blueprint.

    This class takes a PIL Image object and converts its pixels into blocks
    within a given blueprint object. Each pixel becomes a block in the blueprint.

    Args:
        bp (smblueprint.Blueprint): The blueprint object to which the picture blocks
            will be added. This object is modified in place.
        image (PIL.Image.Image): The image to convert into blueprint blocks.
        block_type (smblueprint.BlockType, optional): The type of block to use
            for the pixels. Defaults to sm.BlockType.PLASTIC.
    """
    def __init__(self, bp, image, block_type=sm.BlockType.PLASTIC):
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                color_hex = f"{r:02X}{g:02X}{b:02X}"
                bp.add_block(sm.Blocks(x, y, 0, 1, 1, 1, block_type, color_hex))
