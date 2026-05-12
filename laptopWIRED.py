import hid
import serial
import time

port = "/dev/tty.usbmodem101"
baud = 115200
neutral = 1500
maxThrottle = 1600
ds4Vendor = 1356
ds4Product = 1476
deadband = 10

def map_range(value, in_min, in_max, out_min, out_max):
    value = max(in_min, min(value, in_max))
    return out_min + (value - in_min) / (in_max - in_min) * (out_max - out_min)

# Connect to PS4 controller
print("Connecting to DualShock 4...")
gamepad = hid.device()
gamepad.open(ds4Vendor, ds4Product)
gamepad.set_nonblocking(True)
print(f"Connected to: {gamepad.get_product_string()}")

# Connect to Pico
print(f"Opening serial port {port}...")
ser = serial.Serial(port, baud, timeout=1)
print("Waiting 8 seconds for ESC to arm")
time.sleep(8)
print("Left stick = steer, R2 = throttle. Ctrl+C to stop.")

# Main loop
try:
    while True:
        report = gamepad.read(64)
        if report and len(report) > 8:

            # Steering
            lx = report[1]
            lx_centered = lx - 127
            if abs(lx_centered) < deadband:
                lx_centered = 0
            steer = map_range(lx_centered, -127, 127, 0, 180)

            # Throttle
            r2 = report[9]
            if r2 < 20:
                throttle = neutral
            else:
                throttle = map_range(r2, 20, 255, 1560, maxThrottle)

            # Send to Pico
            cmd = f"S{steer:.1f},T{throttle:.0f}\n"
            ser.write(cmd.encode())

            print(f"Steer: {steer:.1f}°  Throttle: {throttle:.0f}µs  R2: {r2}", end="\r")

        time.sleep(0.02)

# Shutdown
except KeyboardInterrupt:
    print("\nStopping — sending neutral.")
    ser.write(f"S90.0,T{neutral}\n".encode())
    ser.close()
    gamepad.close()