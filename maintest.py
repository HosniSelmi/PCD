import time
import pyfirmata

board = pyfirmata.Arduino('COM4')

# Define pins
bus_voltage_1_pin = board.get_pin('a:0:i')
current_1_pin = board.get_pin('a:1:i')
bus_voltage_2_pin = board.get_pin('a:2:i')
current_2_pin = board.get_pin('a:3:i')
bus_voltage_3_pin = board.get_pin('a:4:i')
current_3_pin = board.get_pin('a:5:i')

# Wait for the board to be ready

# Main loop
while True:
    # Read analog pins and calculate power
    bus_voltage_1 = bus_voltage_1_pin.read() * 5.0
    current_1 = current_1_pin.read() * 1000.0
    power_1 = bus_voltage_1 * current_1

    bus_voltage_2 = bus_voltage_2_pin.read() * 5.0
    current_2 = current_2_pin.read() * 1000.0
    power_2 = bus_voltage_2 * current_2

    bus_voltage_3 = bus_voltage_3_pin.read() * 5.0
    current_3 = current_3_pin.read() * 1000.0
    power_3 = bus_voltage_3 * current_3

    # Print results
    print(power_1, power_2, power_3)

    # Wait for 3 seconds before reading again
    time.sleep(3)
