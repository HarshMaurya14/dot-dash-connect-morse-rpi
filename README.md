# Dot Dash Connect – Morse Code Encoder/Decoder on Raspberry Pi

A Raspberry Pi project that converts **text to Morse code** (shown on LEDs and a buzzer) and **Morse code to text** (entered with push buttons). Built in Python with `RPi.GPIO` as a second-year Mini Project (SY Sem-IV, Electronics & Telecommunication Engineering, Pillai College of Engineering, University of Mumbai, A.Y. 2024-25).

## Features
- **Encode mode:** type text, the Pi plays it as Morse using a red LED (dot), green LED (dash), yellow LED (space) and a buzzer.
- **Decode mode:** enter dots, dashes and spaces with three push buttons; the Pi translates them to text live.
- **Interrupt-driven input:** button presses are handled with GPIO event detection, with software debouncing.
- **Error handling:** invalid Morse sequences are reported, and GPIO is cleaned up on exit (Ctrl+C).

## Hardware
- Raspberry Pi
- 3 LEDs (red, green, yellow) with resistors
- 3 push buttons
- Buzzer
- Breadboard and jumper wires

### Pin mapping (BCM)
| Component | GPIO |
|---|---|
| Red LED (dot) | 17 |
| Green LED (dash) | 27 |
| Yellow LED (space) | 22 |
| Dot button | 5 |
| Dash button | 6 |
| Space button | 13 |
| Buzzer | 18 |

Buttons use the internal pull-up resistors (`GPIO.PUD_UP`) and trigger on a falling edge.

## How to run
```bash
sudo apt install python3-rpi.gpio   # usually preinstalled on Raspberry Pi OS
sudo python3 morse_code.py
```
Then enter `E` to encode text, or `D` to decode using the buttons.

## Concepts demonstrated
GPIO input/output, pull-up resistors, interrupts and callbacks, button debouncing, timing control for dot/dash durations, signal handling, hardware–software integration.

## Project report
See [`docs/Dot_Dash_Connect_Report.pdf`](docs/Dot_Dash_Connect_Report.pdf) for the full report (block diagram, circuit diagram, hardware and software description).

## Note
The project title in the report says "Secure Morse Messaging", but the encoder is a plain text-to-Morse conversion and does not use cryptography.

## Team
Team project (5 members): Mahak Kumari, Harsh Maurya, Aniket Merwade, Aditya Mhatre, Neetu Pal. Guide: Prof. Ishmeet Singh Riar.

**My contribution:** _(edit this line: e.g. wiring the circuit, writing the Python code, testing, report)_

## Possible extensions
Wireless transmission of Morse messages, an LCD display for decoded text, and integration with other communication devices.
