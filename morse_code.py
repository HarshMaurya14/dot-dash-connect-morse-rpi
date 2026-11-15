"""
Dot Dash Connect - Morse Code Encoder/Decoder on Raspberry Pi

Encode mode : type text -> Morse is played on LEDs + buzzer.
Decode mode : press the dot / dash / space buttons -> text is built up.

Run on a Raspberry Pi:  sudo python3 morse_code.py
"""
import time
from signal import signal, SIGINT
from sys import exit

import RPi.GPIO as GPIO

# ---------------- Pin definitions (BCM numbering) ----------------
LED_DOT = 17     # Red LED    - dot
LED_DASH = 27    # Green LED  - dash
LED_SPACE = 22   # Yellow LED - space
BUTTON_DOT = 5
BUTTON_DASH = 6
BUTTON_SPACE = 13
BUZZER = 18

# ---------------- Morse code dictionary ----------------
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.',
}

# ---------------- Timing constants ----------------
DOT_DURATION = 0.1    # seconds
DASH_DURATION = 0.3   # seconds
DEBOUNCE_TIME = 150   # milliseconds

# ---------------- GPIO setup ----------------
GPIO.setmode(GPIO.BCM)
GPIO.setup([LED_DOT, LED_DASH, LED_SPACE], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([BUTTON_DOT, BUTTON_DASH, BUTTON_SPACE], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER, GPIO.OUT, initial=GPIO.LOW)

# ---------------- Data variables ----------------
morse_input = ""
translated_text = ""


# ---------------- Encoding (text -> Morse) ----------------
def encrypt_to_morse(text):
    """Convert text to a Morse string (letters separated by space, words by ' / ')."""
    encrypted_text = ""
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            encrypted_text += MORSE_CODE_DICT[char] + " "
        elif char == " ":
            encrypted_text += " / "  # separator for words
    return encrypted_text.strip()


def encryption_mode():
    text = input("Enter text to encrypt: ")
    morse_code = encrypt_to_morse(text)
    print(f"Encrypted Morse Code: {morse_code}")

    for symbol in morse_code:
        if symbol == ".":
            GPIO.output(LED_DOT, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(DOT_DURATION)
        elif symbol == "-":
            GPIO.output(LED_DASH, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(DASH_DURATION)
        elif symbol == " ":
            GPIO.output(LED_SPACE, GPIO.HIGH)
            time.sleep(0.3)

        # Turn off all indicators
        GPIO.output(LED_DOT, GPIO.LOW)
        GPIO.output(LED_DASH, GPIO.LOW)
        GPIO.output(LED_SPACE, GPIO.LOW)
        GPIO.output(BUZZER, GPIO.LOW)
        time.sleep(0.1)


# ---------------- Decoding (buttons -> text) ----------------
def dot_callback(channel):
    global morse_input
    morse_input += "."
    GPIO.output(LED_DOT, GPIO.HIGH)
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(DOT_DURATION)
    GPIO.output(LED_DOT, GPIO.LOW)
    GPIO.output(BUZZER, GPIO.LOW)
    update_display()


def dash_callback(channel):
    global morse_input
    morse_input += "-"
    GPIO.output(LED_DASH, GPIO.HIGH)
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(DASH_DURATION)
    GPIO.output(LED_DASH, GPIO.LOW)
    GPIO.output(BUZZER, GPIO.LOW)
    update_display()


def space_callback(channel):
    global morse_input, translated_text
    GPIO.output(LED_SPACE, GPIO.HIGH)
    if morse_input in MORSE_CODE_DICT.values():
        translated_text += list(MORSE_CODE_DICT.keys())[
            list(MORSE_CODE_DICT.values()).index(morse_input)
        ]
    elif morse_input == "":
        translated_text += " "
    else:
        print("Invalid Code")
    morse_input = ""
    GPIO.output(LED_SPACE, GPIO.LOW)
    update_display()


def update_display():
    print(f"Input: {morse_input} | Translation: {translated_text}")


# ---------------- Button interrupts ----------------
GPIO.add_event_detect(BUTTON_DOT, GPIO.FALLING, callback=dot_callback, bouncetime=DEBOUNCE_TIME)
GPIO.add_event_detect(BUTTON_DASH, GPIO.FALLING, callback=dash_callback, bouncetime=DEBOUNCE_TIME)
GPIO.add_event_detect(BUTTON_SPACE, GPIO.FALLING, callback=space_callback, bouncetime=DEBOUNCE_TIME)


# ---------------- Graceful exit ----------------
def handler(signal_received, frame):
    GPIO.cleanup()
    exit(0)


signal(SIGINT, handler)

# ---------------- Main loop ----------------
try:
    print("Morse Code System Ready")
    while True:
        mode = input("Enter 'E' for Encryption or 'D' for Decryption: ").strip().upper()
        if mode == 'E':
            encryption_mode()
        elif mode == 'D':
            print("Decryption Mode Active. Use Buttons to Input Morse Code.")
        else:
            print("Invalid choice. Please enter 'E' or 'D'.")
        time.sleep(0.1)

except KeyboardInterrupt:
    handler(None, None)
except Exception as e:
    print(f"Unexpected Error: {e}")
    handler(None, None)
