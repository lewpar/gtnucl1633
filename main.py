from gtnucl1633 import GTNUCL1633
import time

sensor = GTNUCL1633(port="/dev/serial0", 
                    baud_rate=115200, 
                    debug=False)

print ("Initializing sensor..")
sensor.open()
print ("> Done\n")

time.sleep(0.1)

print("Fetching firmware information..")
print(f"> Firmware Version: {sensor.get_firmware_version()}, Release: {sensor.get_firmware_release_date()}\n")

time.sleep(0.1)

print("Fetching number of fingerprints stored on sensor..")
print(f"> {sensor.get_user_count()} fingerprints stored.\n")

time.sleep(0.1)

print("Fetching next available user id..")
print(f"> {sensor.get_entry_id()} is the next available id.\n")

time.sleep(0.1)

print("Waiting for touch inputs..")

while True:
    is_finger_touching = sensor.is_press_finger()

    if is_finger_touching:
        sensor.switch_led_on()

        step = 1

        print("Ready for enrolment, press enter to start training..")
        print("Ensure you finger is on the sensor.")

        free_user_id = sensor.get_entry_id()

        _ = input()
        sensor.start_enrolment(free_user_id)

        while sensor.is_enrolling():
            print(f"Ready for next enrolment stage ({step}/{sensor.get_total_enrolment_stages()}), ")
            _ = input()

            (enrol_result, enrol_progress) = sensor.continue_enrolment()
            step = enrol_progress

            if not enrol_result:
                ack = sensor.get_last_acknowledgement()
                print(f"Failed to enrol, terminating enrolment. ACK: {hex(ack)}")
    else:
        sensor.switch_led_off()

    time.sleep(0.1)

#Terminate
sensor.close()