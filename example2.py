import smblueprint as sm
from PIL import Image

# Load and resize image
img = Image.open("michael_rosen_with_lips_for_eyes.png").convert("RGB")

bp = sm.Blueprint()

comp.picture(bp, img, sm.BlockType.METAL1)

bp.write("blueprint.json")