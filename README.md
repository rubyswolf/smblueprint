# smBlueprint Library

A Python library to create blueprints for (presumably) a game or application that uses a block-based building system.

## Installation

1.  Clone this repository.
2.  Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Components

### Picture Component

The `picture` component allows you to convert an image file into a blueprint of colored blocks.

**Usage:**

The `smblueprint.components.picture` class takes a `Blueprint` object, a PIL Image object, and an optional `BlockType` as input. It modifies the `Blueprint` object by adding blocks that represent the pixels of the image.

**Example:**

See `example.py` for a demonstration of how to use the `picture` component.

To run the example:
```bash
python example.py
```
This will generate a `picture_blueprint.json` file representing a simple 16x16 image.

**How it works:**

The `example.py` script:
1. Creates a `Blueprint` instance.
2. Generates a sample 16x16 image using the Pillow library (a red square with a blue dot).
3. Initializes the `picture` component with the blueprint and the sample image. The component iterates through each pixel of the image and adds a corresponding colored block to the blueprint.
4. Saves the resulting blueprint to `picture_blueprint.json`.

You can adapt `example.py` to load your own images and customize the block types.
