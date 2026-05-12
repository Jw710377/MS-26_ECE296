from machine import Pin, PWM
import utime
import sys

led = Pin("LED", Pin.OUT)

def blink(n, fast=False):
    delay = 100 if fast else 400
    for _ in range(n):
        led.on()
        utime.sleep_ms(delay)
        led.off()
        utime.sleep_ms(delay)
    utime.sleep_ms(500)

# Indicates RP Pico Booted correctly
blink(1)

# Pins
esc = PWM(Pin(1))
servo = PWM(Pin(0))
esc.freq(50)
servo.freq(50)

neutral = 1500
maxThrottle = 1600

# Functions
def setThrottle(us):
    us = max(neutral, min(int(us), maxThrottle))
    esc.duty_u16(int(us / 20000 * 65535))

def setSteering(degrees):
    degrees = max(0, min(int(degrees), 180))
    minUs = 500
    maxUs = 2500
    us = min_us + (degrees / 180) * (maxUs - minUs)
    servo.duty_u16(int(us / 20000 * 65535))

# PWM init ok
blink(2)

# Arming ESC
blink(3)
esc.duty_u16(int(neutral / 20000 * 65535))
utime.sleep(4)

# ESC Armed
blink(4)
set_steering(90)
set_throttle(neutral)
utime.sleep(2)

# Entering main loop
led.on()

# Main loop
while True:
    try:
        line = sys.stdin.readline().strip()
        if not line:
            continue
        if line.startswith("S") and "," in line:
            parts = line.split(",")
            steer = float(parts[0][1:])
            throttle = float(parts[1][1:])
            setSteering(steer)
            setThrottle(throttle)
            # Flickers with a command
            led.toggle() 
    except Exception as e:
        # rapid blinks = error in main loop
        blink(10, fast=True)