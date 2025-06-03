from PIL import Image, ImageDraw
from smblueprint import Blueprint, BlockType
from smblueprint.components import picture # Corrected import

# 1. Create a blueprint object
# This initializes an empty Scrap Mechanic blueprint.
# The `Blueprint` class is the main container for all blueprint parts.
bp = Blueprint()

# 2. Create a sample image using Pillow (PIL)
# This section demonstrates how to create an image that will be converted into blueprint blocks.
# We're creating a 16x16 pixel image.
img_size = 16
# Initialize the image with a red background. "RGB" mode means 3 channels (Red, Green, Blue).
img = Image.new("RGB", (img_size, img_size), "red")
# Create a drawing context to modify the image.
draw = ImageDraw.Draw(img)
# Draw a blue circle in the middle of the red square.
# The coordinates define the bounding box of the ellipse: (x0, y0, x1, y1).
draw.ellipse((img_size // 4, img_size // 4, img_size * 3 // 4, img_size * 3 // 4), fill="blue")

# 3. Instantiate the picture component to convert the image to blueprint blocks
# The `picture` component takes the blueprint object (`bp`) and the Pillow image (`img`).
# It iterates through each pixel of the image and adds a corresponding block to the blueprint.
# The `block_type` argument specifies what kind of Scrap Mechanic block to use (e.g., PLASTIC, WOOD, METAL).
# This operation modifies the `bp` object in place, adding new parts (blocks) to it.
pic_component = picture(bp, img, block_type=BlockType.PLASTIC)

# 4. Write the blueprint to a JSON file
# This saves the blueprint data (including the newly added picture blocks) to a file.
# The resulting file is in the format that Scrap Mechanic can understand.
output_filename = "picture_blueprint.json"
bp.write(output_filename)

# Print confirmation messages
print(f"Blueprint saved to {output_filename}")
# Display the total number of parts (blocks) in the blueprint.
# For a 16x16 image, this should be 16*16 = 256 parts.
print(f"The blueprint contains {len(bp.parts)} parts.")

# Verification step:
# To verify the output, you can open 'picture_blueprint.json' in a text editor.
# You should see a JSON structure where each block corresponds to a pixel from the image,
# with appropriate colors and positions.
# The example image (red square with a blue dot) should be recognizable in the block data.
