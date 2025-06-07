import keyboard
import time
import sys

# Track switch states (False = off, True = on)
switches = [False] * 8

def set_switches_from_char(char):
    code = ord(char)
    bits = [(code >> i) & 1 for i in range(8)]
    return bits

def press_switches(bits):
    # For each switch, press key if bit is 1, release if 0
    for i, bit in enumerate(bits):
        key = str(i + 1)
        if switches[i] != bool(bit):
            keyboard.press_and_release(key)
            switches[i] = bool(bit)
            time.sleep(0.05)  # Small delay to ensure key is registered

def main():
    print("Press any key (letter/number/symbol) to set switches. ESC to exit.")
    while True:
        event = keyboard.read_event(suppress=True)  # Suppress all key events
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'esc':
                print("Exiting.")
                sys.exit(0)
            elif event.name == 'backspace':
                keyboard.press('0')
                time.sleep(0.05)  # 1/20th of a second
                keyboard.release('0')
                print("Pressed 0 for Backspace")
            elif len(event.name) == 1 or event.name == 'space':
                char = ' ' if event.name == 'space' else event.name
                bits = set_switches_from_char(char)
                press_switches(bits)
                keyboard.press('9')
                time.sleep(0.05)  # 1/20th of a second
                keyboard.release('9')
                print(f"Set switches to {bits} for '{char}' (code {ord(char)})")

if __name__ == "__main__":
    main()