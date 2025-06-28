from gtnucl1633 import GTNUCL1633
import time

sensor = GTNUCL1633(port="/dev/serial0", 
                    baud_rate=115200, 
                    debug=False)

class MenuItem:
    def __init__(self, title, delegate):
        self.title = title
        self.delegate = delegate

running = True

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

def exit_loop():
    global running
    running = False
    print("Exiting..")

def train_finger():
    is_finger_touching = sensor.is_press_finger()

    if not is_finger_touching:
        print("Place your finger on the sensor to begin.")

    while not sensor.is_press_finger():
        time.sleep(0.1)

    sensor.switch_led_on()

    step = 1

    print("Ready for enrolment, press enter to start training..")

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
            print(f"Failed to enrol, terminating enrolment. ACK: {sensor.get_ack_message(ack)}")

def test_finger():
    is_finger_touching = sensor.is_press_finger()

    if not is_finger_touching:
        print("Place your finger on the sensor to begin.")

    while not sensor.is_press_finger():
        time.sleep(0.1)

    print("Identifying fingerprint, please leave your finger on the sensor..")
    sensor.switch_led_on()
    user_id = sensor.identify()
    sensor.switch_led_off()

    if user_id < 0:
        print("No identity found\n")

        return
    print(f"Identified user: {user_id}")

menu = {
    1: MenuItem("Train Finger", train_finger),
    2: MenuItem("Test Finger", test_finger),
    3: MenuItem("Exit", exit_loop)
}

def get_selection(prompt: str) -> None | int:
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            return None

while running:

    for entry in menu:
        item = menu[entry]
        print(f"{entry}: {item.title}")

    selection = get_selection("Enter selection (int): ")

    if selection == None:
        print("Please enter a valid integer.")
        continue

    selected_menu = menu[selection]
    selected_menu.delegate()

    time.sleep(0.1)

#Terminate
sensor.close()


