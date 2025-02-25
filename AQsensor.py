'''
import time
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import math

# Configuration
SAMPLE_RATE = 1  # Readings per second
WARM_UP_TIME = 12 # Seconds
VCC = 3.3  # Reference voltage (3.3V)
RL = 20000  # Load resistance (10k ohms)
R0 = 10  # Replace with your sensor's R0 in clean air
GAS_RATIO_CLEAN_AIR = 1  # Replace with your sensor's Rs/R0 in clean air

# Gas calibration constants (these need to be updated based on sensor calibration or datasheet)
GAS_CALIBRATION = {
    'CO2': {'a': -0.72, 'b': 1.54},  # Example for CO2, update for other gases
    'NH3': {'a': -0.75, 'b': 1.60},  # Example for NH3, update accordingly
    'NOx': {'a': -0.78, 'b': 1.62},  # Example for NOx, update accordingly
    'Alcohol': {'a': -0.80, 'b': 1.65},  # Example for Alcohol, update accordingly
    'Benzene': {'a': -0.70, 'b': 1.55},  # Example for Benzene, update accordingly
    'Smoke': {'a': -0.77, 'b': 1.61}  # Example for Smoke, update accordingly
}

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
channel = AnalogIn(ads, ADS.P0)

def calculate_rs_r0(voltage):
    """Calculates Rs/R0 ratio."""
    try:
        rs = ((VCC * RL) / voltage) - RL
        rs_r0 = rs / R0
        return rs_r0
    except ZeroDivisionError:
        return 0  # Handle potential division by zero

def calculate_ppm(rs_r0, gas_type='CO2'):
    """Calculates PPM for different gases."""
    if gas_type not in GAS_CALIBRATION:
        print("Unknown gas type, defaulting to CO2")
        gas_type = 'CO2'

    # Use the corresponding calibration constants for the selected gas
    a = GAS_CALIBRATION[gas_type]['a']
    b = GAS_CALIBRATION[gas_type]['b']

    try:
        ppm = 10 ** (a * math.log10(rs_r0) + b)
        return ppm
    except (ValueError, OverflowError):
        return 0 # Handle potential math errors.

def get_r0():
    """Gets R0 in clean air"""
    print("Please provide clean air for 2 minutes to calibrate the sensor")
    time.sleep(WARM_UP_TIME)
    total_rs = 0
    num_samples = 60
    for _ in range(num_samples):
        voltage = channel.voltage
        rs = ((VCC * RL) / voltage) - RL
        total_rs += rs
        time.sleep(1)
    average_rs = total_rs / num_samples
    calculated_r0 = average_rs / GAS_RATIO_CLEAN_AIR
    return calculated_r0

def main():
    global R0 # Allow R0 to be changed
    R0 = get_r0() # Get R0 value in clean air

    print("Starting air quality monitoring...")
    try:
        while True:
            voltage = channel.voltage
            rs_r0 = calculate_rs_r0(voltage)

            # You can specify the gas to measure here, e.g., 'CO2', 'NH3', etc.
            ppm = calculate_ppm(rs_r0, gas_type='CO2')

            print(f"Voltage: {voltage:.3f}V | Rs/R0: {rs_r0:.3f} | Estimated CO2 PPM: {ppm:.2f}")

            time.sleep(1 / SAMPLE_RATE)

    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()

    '''


import time
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import math

# Configuration
SAMPLE_RATE = 1  # Readings per second
WARM_UP_TIME = 12  # Seconds
VCC = 3.3  # Reference voltage (3.3V)
RL = 20000  # Load resistance (20k ohms)
R0 = 1.5  # Initial placeholder, will be calibrated
GAS_RATIO_CLEAN_AIR = 1  # Assumed Rs/R0 in clean air

# Gas calibration constants (these need to be updated based on sensor calibration or datasheet)
GAS_CALIBRATION = {
    'CO2': {'a': -0.72, 'b': 1.54},
    'NH3': {'a': -0.75, 'b': 1.60},
    'NOx': {'a': -0.78, 'b': 1.62},
    'Alcohol': {'a': -0.80, 'b': 1.65},
    'Benzene': {'a': -0.70, 'b': 1.55},
    'Smoke': {'a': -0.77, 'b': 1.61}
}

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
channel = AnalogIn(ads, ADS.P0)

def calculate_rs_r0(voltage):
    """Calculates Rs/R0 ratio."""
    try:
        rs = ((VCC * RL) / voltage) - RL
        rs_r0 = rs / R0
        return rs_r0
    except ZeroDivisionError:
        return 0  # Handle potential division by zero

def calculate_ppm(rs_r0, gas_type='CO2'):
    """Calculates PPM for different gases."""
    if gas_type not in GAS_CALIBRATION:
        print("Unknown gas type, defaulting to CO2")
        gas_type = 'CO2'

    a = GAS_CALIBRATION[gas_type]['a']
    b = GAS_CALIBRATION[gas_type]['b']

    try:
        ppm = 10 ** (a * math.log10(rs_r0) + b)
        return ppm
    except (ValueError, OverflowError):
        return 0  # Handle potential math errors.

def get_r0():
    """Gets R0 in clean air"""
    print("Please provide clean air for 1 minutes to calibrate the sensor")
    time.sleep(WARM_UP_TIME)
    total_rs = 0
    num_samples = 60
    for _ in range(num_samples):
        voltage = channel.voltage
        rs = ((VCC * RL) / voltage) - RL
        total_rs += rs
        time.sleep(1)
    average_rs = total_rs / num_samples
    calculated_r0 = average_rs / GAS_RATIO_CLEAN_AIR
    return calculated_r0

def main():
    global R0  # Allow R0 to be changed
    R0 = get_r0()  # Get R0 value in clean air
    print(f"R0 Calibrated to {R0:.2f}")

    print("Starting air quality monitoring...")
    try:
        while True:
            voltage = channel.voltage
            rs_r0 = calculate_rs_r0(voltage)

            # Calculate PPM for all gases
            co2_ppm = calculate_ppm(rs_r0, gas_type='CO2')
            nh3_ppm = calculate_ppm(rs_r0, gas_type='NH3')
            nox_ppm = calculate_ppm(rs_r0, gas_type='NOx')
            alcohol_ppm = calculate_ppm(rs_r0, gas_type='Alcohol')
            benzene_ppm = calculate_ppm(rs_r0, gas_type='Benzene')
            smoke_ppm = calculate_ppm(rs_r0, gas_type='Smoke')

            print(f"Voltage: {voltage:.3f}V | Rs/R0: {rs_r0:.3f}")
            print(f"Estimated CO2 PPM: {co2_ppm:.2f} | NH3 PPM: {nh3_ppm:.2f} | NOx PPM: {nox_ppm:.2f} | Alcohol PPM: {alcohol_ppm:.2f} | Benzene PPM: {benzene_ppm:.2f} | Smoke PPM: {smoke_ppm:.2f}")

            time.sleep(1 / SAMPLE_RATE)

    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()