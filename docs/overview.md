# GTNUCL1633 Wiki

## Overview

The `GTNUCL1633` class is a Python driver for the GTNUCL1633 Fingerprint Reader. It provides a high-level interface for communicating with the fingerprint sensor, enrolling and identifying fingerprints, and managing the sensor's database.

- **Repository:** [main.py](../main.py) for usage examples.
- **Device:** [GTNUCL1633 Fingerprint Reader](https://cdn.sparkfun.com/assets/0/4/f/d/9/GT-nucl1633k1_product_specification_v1.2_20220509.pdf)
- **Programming Guide:** [Official Guide](https://cdn.sparkfun.com/assets/1/4/5/e/7/GT-NUCL1633K1_Programming_guide_V1.3.pdf)

## Features
- Open/close sensor communication
- LED control
- Fingerprint enrollment and identification
- User management (add, delete, count)
- Firmware and sensor info retrieval
- UART baud rate configuration

## Usage Example
```python
from gtnucl1633 import GTNUCL1633
import time

sensor = GTNUCL1633(port="/dev/serial0", baud_rate=115200, debug=False)
sensor.open()
print(f"Firmware Version: {sensor.get_firmware_version()}, Release: {sensor.get_firmware_release_date()}")
print(f"Fingerprints stored: {sensor.get_user_count()}")

# Enroll a new fingerprint
user_id = sensor.get_entry_id()
success = sensor.start_enrolment(user_id)
if success:
    print("Enrolment started. Follow sensor prompts.")

# Identify a fingerprint
if sensor.is_press_finger():
    identified_id = sensor.identify()
    print(f"Identified user: {identified_id}")

sensor.close()
```
