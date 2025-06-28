from gtnucl1633 import GTNUCL1633
import time

sensor = GTNUCL1633(port="/dev/serial0", baud_rate=115200, debug=False)

# Initialize Sensor
sensor.open()

free_id = sensor.get_entry_id()

if free_id < 0:
    print("Failed to get free id.")
else:
    print(f"Got free id: {free_id}")

print("Waiting for touch inputs..")

count = sensor.get_user_count()
print(count)

while True:
    is_finger_touching = sensor.is_press_finger()

    if is_finger_touching:
        sensor.switch_led_on()
        user_id = sensor.identify()
        print(f"Identified user id: {user_id}")
    else:
        sensor.switch_led_off()

    time.sleep(0.1)

# Terminate
sensor.close()


