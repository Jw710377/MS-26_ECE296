# MS-26_ECE296
Controls an RC car using a PS4 controller connected to a laptop, which sends commands to a Raspberry Pi Pico W. The Pico drives the motor (throttle) and servo (steering).

Setup
1. Flash the Pico
Open mainWIRED.py in Thonny
Save to Pico W as main.py
It will run automatically on power-on

2. Pair the PS4 Controller
Hold SHARE + PS until the light bar flashes white
Pair via Bluetooth in your laptop's system settings

3. Find the Pico's serial port
ls /dev/tty.usbmodem*
Update the port variable in laptopWIRED.py to match.

4. Run the laptop script
python3 laptopWIRED.py
Wait 8 seconds for the ESC to arm, then drive.

Controls
InputActionLeft stick left/rightSteeringR2 triggerThrottle (forward)Ctrl+CStop — returns to neutral

LED Status (Pico W)
1 slow blink: Boot OK
2 slow blinks: PWM init OK
3 slow blinks: Arming ESC
4 slow blinks: ESC armedSolid ONWaiting for commands
Flickering: Commands being received
10 rapid blinks: Error in main loop

Variables
mainWIRED.py
neutral: neutral pulse width 
maxThrottle: Maximum throttle pulse width

laptopWIRED.py
port: serial port
neutral: neutral pulse width
maxThrottle: Maximum throttle
deadband: ignores small movements near center
