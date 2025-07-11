import serial
import datetime
import time

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

# Controls the UART BAUD rate
CMD_UART_CONTROL = 0xA3

CMD_UART_CONTROL_BAUD_9600 = 0x1
CMD_UART_CONTROL_BAUD_19200 = 0x2
CMD_UART_CONTROL_BAUD_115200 = 0x3
CMD_UART_CONTROL_BAUD_230400 = 0x4
CMD_UART_CONTROL_BAUD_460800 = 0x5
CMD_UART_CONTROL_BAUD_921600 = 0x6

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
        """
        Initialize the GTNUCL1633 fingerprint sensor interface.

        Parameters:
            port (str): Serial port to use for communication.
            baud_rate (int): Baud rate for serial communication.
            timeout (float): Read timeout for serial communication.
            debug (bool): If True, prints debug information.
        """
        self.device = serial.Serial(port, baud_rate, timeout=timeout)
        self.debug = debug
        self.firmware_release_date = None
        self.sensor_type = None
        self.is_training = False
        self.last_ack = None
    
    def __bytes_to_short(self, high: int, low: int) -> int:
        """
        Convert two bytes (high and low) into a single 16-bit integer.

        Parameters:
            high (int): High byte.
            low (int): Low byte.

        Returns:
            int: The combined 16-bit integer.
        """
        return  (high << 8) | low

    def __short_to_bytes(self, value: int) -> tuple[int, int]:
        """
        Convert a 16-bit integer into two separate bytes.

        Parameters:
            value (int): A 16-bit integer value.

        Returns:
            tuple[int, int]: A tuple of (high_byte, low_byte).
        """
        high = (value >> 8) & 0xFF
        low = value & 0xFF
        return high, low
    
    def get_ack_message(self, ack):
        """
        Return a descriptive message string corresponding to a given ACK code.

        Parameters:
            ack (int): The ACK code to look up (e.g., ACK_SUCCESS, ACK_FAIL, etc.).

        Returns:
            str: A human-readable message describing the result of a fingerprint command.
                Returns "Unknown ACK code" if the code is not recognized.
        """
        ack_messages = {
            ACK_SUCCESS: "Command executed successfully",
            ACK_FAIL: "Command execution failed",
            ACK_FULL: "The fingerprint database is full",
            ACK_NOUSER: "The specified ID is not registered",
            ACK_USER_EXIST: "The specified ID is already registered",
            ACK_TIMEOUT: "Timeout occurred while capturing the finger",
            ACK_WRONG_FORMAT: "The fingerprint template has a wrong format",
            ACK_BREAK: "Command was aborted",
            ACK_INVALID_PARAMETER: "An invalid parameter was provided",
            ACK_FINGER_IS_NOT_PRESSED: "Finger is not pressed on the sensor",
            ACK_COMMAND_NO_SUPPORT: "Command is not supported by the device",
            ACK_ENROLL_OVEREXPOSURE: "Finger image is overexposed during enrollment",
            ACK_ENROLL_MOVE_MORE: "Finger moved too little during enrollment",
            ACK_ENROLL_MOVE_LESS: "Finger moved too much during enrollment",
            ACK_ENROLL_DUPLICATE: "Duplicate finger position detected during enrollment",
            ACK_FINGER_PRESS_NOT_FULL: "Finger was not fully pressed on the sensor",
            ACK_ENROLL_POOR_QUALITY: "Finger image quality is too poor for enrollment",
        }

        return ack_messages.get(ack, "Unknown ACK code")

    def get_last_acknowledgement(self) -> None | int:
        """
        Gets the last acknowledgement received from the sensor.

        Returns:
            (None | int): The acknowledgement id. Returns `None` if no acknowledgement was received.
        """
        return self.last_ack
    
    def get_sensor_type(self) -> None | int:
        """
        Get the sensor type fo the GTNUCL1633.

        The documentation is not exactly clear on what the types are.

        Returns:
            (None | int): The sensor type. Returns `None` if `open` has not been called.
        """
        return self.sensor_type

    def get_firmware_release_date(self) -> None | datetime.date:
        """
        Get the release date for the firmware on the sensor.

        Returns:
            (None | datetime.date): The firmware release date. Returns `None` if `open` has not been called.
        """
        return self.firmware_release_date
    
    def get_firmware_version(self) -> None | int:
        """
        Get the firmware version on the sensor.

        Returns:
            (None | int): The version of the firmware. Returns `None` if command failed.
        """
        self.send_command(CMD_GET_FIRMWARE_VERSION)
        response = self.read_response()

        len_high = response[2]
        len_low = response[3]
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            return None
        
        # Version Data length + start code, checksum and end code (3 bytes).
        data_len = self.__bytes_to_short(len_high, len_low) + 3
        version_data = self.read_response(data_len)

        version = version_data[5]

        return version

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

        # Data length + start code, checksum and end code (3 bytes).
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

        self.last_ack = None

    def close(self):
        """
        Terminates the serial communication.

        Returns:
            None: 
        """
        self.send_command(CMD_CLOSE)

        self.last_ack = None

    def send_command(self, command, param1 = 0, param2 = 0, param3 = 0, param4 = 0):
        checksum = command ^ param1 ^ param2 ^ param3 ^ param4

        # Input payloads are always sandwiched between 0xF5, this is the same for responses.
        payload = bytes([ 0xF5, command, param1, param2, param3, param4, checksum, 0xF5 ])

        if self.debug:
            print(f"Tx: {payload}")

        self.device.write(payload)
        time.sleep(0.25)

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
        self.send_command(CMD_LED_CONTROL, param1=0x1)

        response = self.read_response()
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS and self.debug:
            print("Failed to switch led off.")

    def switch_led_on(self):
        """
        Switches the touch sensor LED on.
        
        Returns:
            None:
        """
        self.send_command(CMD_LED_CONTROL, param1=0x0)

        response = self.read_response()
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS and self.debug:
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
        ack = response[4]

        self.last_ack = ack

        return status == 1
    
    def get_entry_id(self) -> None | int:
        """
        Gets a free user id for fingerprint training.

        Returns:
            (int | None): The free id. Returns `None` if the command fails or the fingerprint database is full.
        """
        self.send_command(CMD_GET_ENTRY_ID)
        response = self.read_response()

        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            return None
        
        high_byte = response[2]
        low_byte = response[3]

        user_id = (high_byte << 8) | low_byte

        return user_id
    
    def get_user_count(self) -> None | int:
        """
        Gets the amount of trained finger prints (users).

        Returns:
            (None | int): The amount of users. Returns `None` if no users or the command fails.
        """
        self.send_command(CMD_GET_USER_COUNT)
        response = self.read_response()

        ack = response[4]

        self.last_ack = ack
        
        if ack != ACK_SUCCESS:
            return None
        
        count_high = response[2]
        count_low = response[3]

        count = self.__bytes_to_short(count_high, count_low)

        return count
    
    def identify(self) -> None | int:
        """
        Identifies the fingerprint (user) currently on the sensor.

        Returns:
            (None | int): The user id. Returns `None` if no user is found or the command failed.
        """
        self.send_command(CMD_IDENTIFY)
        response = self.read_response()

        id_high = response[2]
        id_low = response[3]

        user_id = self.__bytes_to_short(id_high, id_low)

        ack = response[4]

        self.last_ack = ack

        if user_id == 0:
            if ack == ACK_NOUSER:
                return None
            
            if ack == ACK_FAIL:
                return None

        return user_id
    
    def get_total_enrolment_stages(self):
        return 8
    
    def is_enrolling(self):
        return self.is_training
    
    def start_enrolment(self, user_id) -> int:
        """
        Starts the enrolment / training process for a fingerprint (user).

        Returns:
            bool: Returns `True` on success.
        """
        (user_high, user_low) = self.__short_to_bytes(user_id)
        self.send_command(CMD_ENROLL, param1=user_high, param2=user_low)

        response = self.read_response()
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            return False
        
        self.is_training = True
        
        return True
    
    def continue_enrolment(self):
        """
        Continues the enrolment process for a fingerprint (user).
        Returns:
            (bool, int): Returns a tuple indicating if the enrolment step was successful and the enrolment step progress.
        """
        if not self.is_training:
            if self.debug:
                print("You must start an enrolment before you can continue one.")
            return
        
        self.send_command(CMD_ENROLL)
        response = self.read_response()

        if len(response) == 0:
            return (False, 0)

        result = response[1]
        progress = response[2]
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            if ack == ACK_ENROLL_OVEREXPOSURE:
                return (False, progress)
            
            if ack == ACK_ENROLL_MOVE_MORE:
                return (False, progress)
            
            if ack == ACK_ENROLL_MOVE_LESS:
                return (False, progress)
            
            if ack == ACK_ENROLL_DUPLICATE:
                return (False, progress)
            
            self.is_training = False
            return (False, progress)

        # 0x03 = Final Enrolment Complete
        if result == 0x03:
            self.is_training = False
            return (True, progress)

        return (True, progress)
    
    def cancel_enrollment(self, user_id):
        """
        Cancels the enrollment of finger print id (user) and erases it.

        Returns:
            bool: True if cancel was successful.
        """
        (user_high, user_low) = self.__short_to_bytes(user_id)
        self.send_command(CMD_ENROLL_CANCEL, param1=user_high, param2=user_low)
        response = self.read_response()
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            return False
        
        return True

    def delete_all_users(self):
        """
        Deletes all fingerprints (users) stored on the fingerprint sensor.

        Returns:
            bool: True if delete was successful.
        """
        self.send_command(CMD_DELETE_ALL)
        response = self.read_response()
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            return False
        
        return True
    
    def delete_user(self, user_id):
        """
        Deletes the finger print id (user) from the sensor.

        Returns:
            bool: True if cancel was successful.
        """
        (user_high, user_low) = self.__short_to_bytes(user_id)
        self.send_command(CMD_DELETE_ID, param1=user_high, param2=user_low)
        response = self.read_response()
        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            return False
        
        return True
    
    def set_uart_baud(self, baud_id):
        """
        Sets the serial baud rate of the sensor.

        Use `gtnucl1633.CMD_UART_CONTROL_BAUD_*` provided by this module as the `baud_id`.

        Returns:
            bool: True if command was successful.
        """

        if len(baud_id) > 1:
            self.last_ack = None
            raise Exception("baud_id was more than expected length of 1")

        self.send_command(CMD_UART_CONTROL, param1=baud_id)
        response = self.read_response()

        ack = response[4]

        self.last_ack = ack

        if ack != ACK_SUCCESS:
            return False

        return True