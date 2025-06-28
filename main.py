from gtnucl1633 import GTNUCL1633
import time

sensor = GTNUCL1633(port="/dev/serial0", baud_rate=115200, debug=False)

print ("Initializing sensor..")
sensor.open()
print ("> Done\n")

print("Fetching firmware information..")
print(f"> Firmware Version: {sensor.get_firmware_version()}, Release: {sensor.get_firmware_release_date()}\n")

print("Waiting for touch inputs..")

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


