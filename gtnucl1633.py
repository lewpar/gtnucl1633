import serial
import datetime

# Initialize the fingerprint module
CMD_OPEN = 0xA0

# Terminate the fingerprint module
CMD_CLOSE = 0xA1

# Turn the sensor LED on or off
CMD_LED_CONTROL = 0xB4

# Check if a finger is placed on the sensor
CMD_IS_PRESS_FINGER = 0xB5

# Start the fingerprint enrollment process
CMD_ENROLL = 0x01

# Delete the fingerprint with the specified ID
CMD_DELETE_ID = 0x04

# Delete all fingerprints from the database
CMD_DELETE_ALL = 0x05

# Get the number of enrolled fingerprints
CMD_GET_USER_COUNT = 0x09

# Identify a fingerprint using 1:N matching
CMD_IDENTIFY = 0x0C

# Get an unused fingerprint ID for enrollment
CMD_GET_ENTRY_ID = 0x0D

# Get the firmware version of the sensor
CMD_GET_FIRMWARE_VERSION = 0x26

# Cancel the enrollment process
CMD_ENROLL_CANCEL = 0x92

# Command executed successfully
ACK_SUCCESS = 0x00

# Command execution failed
ACK_FAIL = 0x01

# The fingerprint database is full
ACK_FULL = 0x04

# The specified ID is not registered
ACK_NOUSER = 0x05

# The specified ID is already registered
ACK_USER_EXIST = 0x07

# Timeout occurred while capturing the finger
ACK_TIMEOUT = 0x08

# The fingerprint template has a wrong format
ACK_WRONG_FORMAT = 0x09

# Command was aborted
ACK_BREAK = 0x18

# An invalid parameter was provided
ACK_INVALID_PARAMETER = 0xB0

# Finger is not pressed on the sensor
ACK_FINGER_IS_NOT_PRESSED = 0xB1

# Command is not supported by the device
ACK_COMMAND_NO_SUPPORT = 0xB4

# Finger image is overexposed during enrollment
ACK_ENROLL_OVEREXPOSURE = 0xB5

# Finger moved too little during enrollment
ACK_ENROLL_MOVE_MORE = 0xB6

# Finger moved too much during enrollment
ACK_ENROLL_MOVE_LESS = 0xB7

# Duplicate finger position detected during enrollment
ACK_ENROLL_DUPLICATE = 0xB8

# Finger was not fully pressed on the sensor
ACK_FINGER_PRESS_NOT_FULL = 0xB9

# Finger image quality is too poor for enrollment
ACK_ENROLL_POOR_QUALITY = 0xBA


class GTNUCL1633:
    def __init__(self, port="/dev/serial0", baud_rate=115200, timeout=1, debug=False):
        self.device = serial.Serial(port, baud_rate, timeout=timeout)
        self.debug = debug
        self.firmware_release_date = None
        self.sensor_type = None
    
    def __bytes_to_short(self, high: int, low: int) -> int:
        return  (high << 8) | low
    
    def get_sensor_type(self) -> None | int:
        """
        Get the sensor type fo the GTNUCL1633.

        The documentation is not exactly clear on what the types are.

        Returns:
            int: The sensor type. Returns `None` if `open` has not been called.
        """
        return self.sensor_type

    def get_firmware_release_date(self) -> None | datetime.date:
        """
        Get the release date for the firmware on the sensor.

        Returns:
            datetime.date: The firmware release date. Returns `None` if `open` has not been called.
        """
        return self.firmware_release_date

    def open(self):
        """
        Initializes the touch sensor and fetches the firmware release date and sensor type.

        Returns:
            None: 
        """
        self.send_command(CMD_OPEN, param3=1)

        response = self.read_response()

        fw_high = response[2]
        fw_low = response[3]

        # Data length + start code, checksum and end code (3).
        fw_len = self.__bytes_to_short(fw_high, fw_low) + 3

        fw_response = self.read_response(fw_len)

        day = fw_response[3]
        month = fw_response[4]

        year_low = fw_response[5]
        year_high = fw_response[6]
        year = self.__bytes_to_short(year_high, year_low)

        self.firmware_release_date = datetime.date(year, month, day)

        sensor_type = fw_response[8]
        self.sensor_type = sensor_type

    def close(self):
        """
        Terminates the serial communication.

        Returns:
            None: 
        """
        self.send_command(CMD_CLOSE)

    def send_command(self, command, param1 = 0, param2 = 0, param3 = 0, param4 = 0):
        checksum = command ^ param1 ^ param2 ^ param3 ^ param4

        # Input payloads are always sandwiched between 0xF5, this is the same for responses.
        payload = bytes([ 0xF5, command, param1, param2, param3, param4, checksum, 0xF5 ])

        if self.debug:
            print(f"Tx: {payload}")

        self.device.write(payload)

    def read_response(self, length=8) -> bytes:
        response = self.device.read(length)

        if self.debug:
            print(f"Rx: {response}")

        return response
    
    def switch_led_off(self):
        """
        Switches the touch sensor LED off.

        Returns:
            None:
        """
        self.send_command(CMD_LED_CONTROL, param1=1)

        response = self.read_response()
        result = response[4]

        if result != ACK_SUCCESS and self.debug:
            print("Failed to switch led off.")

    def switch_led_on(self):
        """
        Switches the touch sensor LED on.
        
        Returns:
            None:
        """
        self.send_command(CMD_LED_CONTROL, param1=0)

        response = self.read_response()
        result = response[4]

        if result != ACK_SUCCESS and self.debug:
            print("Failed to switch led on.")

    def is_press_finger(self) -> bool:
        """
        Checks if a finger is current on the touch sensor.

        Returns:
            bool: True if a finger is on the sensor.
        """
        self.send_command(CMD_IS_PRESS_FINGER)
        response = self.read_response()
        status = response[2]

        return status == 1
    
    def get_entry_id(self) -> int:
        """
        Gets a free user id for fingerprint training.

        Returns:
            int: The free id. Returns -1 if the command fails or -2 if the fingerprint database is full.
        """
        self.send_command(CMD_GET_ENTRY_ID)
        response = self.read_response()

        result = response[4]

        if result == ACK_FULL:
            print("Failed to get free id, database full.")
            return -2
        
        if result != ACK_SUCCESS:
            print("Failed to get free id, command failed.")
            return -1
        
        high_byte = response[2]
        low_byte = response[3]

        user_id = (high_byte << 8) | low_byte

        return user_id
    
    def get_user_count(self) -> int:
        """
        Gets the amount of trained finger prints (users).

        Returns:
            int: The amount of users. Returns -1 if no users or -2 if command fails.
        """
        self.send_command(CMD_GET_USER_COUNT)
        response = self.read_response()

        ack = response[4]

        if ack == ACK_NOUSER:
            return -1
        
        if ack != ACK_SUCCESS:
            return -2
        
        count_high = response[2]
        count_low = response[3]

        count = self.__bytes_to_short(count_high, count_low)

        return count
