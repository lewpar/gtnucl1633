# GTNUCL1633 Class API Reference

This page documents the public methods of the `GTNUCL1633` class.

## Constructor

```python
GTNUCL1633(port="/dev/serial0", baud_rate=115200, timeout=1, debug=False)
```
- **port**: Serial port to use (default: "/dev/serial0")
- **baud_rate**: Baud rate for serial communication (default: 115200)
- **timeout**: Serial timeout in seconds (default: 1)
- **debug**: Enable debug output (default: False)

## Methods

### Sensor Management

- `open()`
  - Initializes the sensor and fetches firmware info.
- `close()`
  - Terminates serial communication with the sensor.
- `set_uart_baud(baud_id)`
  - Sets the UART baud rate. Use provided constants (e.g., `CMD_UART_CONTROL_BAUD_115200`).

### LED Control

- `switch_led_on()`
  - Turns the sensor LED on.
- `switch_led_off()`
  - Turns the sensor LED off.

### Fingerprint Operations

- `is_press_finger() -> bool`
  - Checks if a finger is currently on the sensor.
- `get_entry_id() -> int | None`
  - Gets a free user ID for enrollment.
- `get_user_count() -> int | None`
  - Returns the number of enrolled fingerprints.
- `identify() -> int | None`
  - Identifies the fingerprint currently on the sensor.

### Enrollment

- `start_enrolment(user_id) -> bool`
  - Starts the enrollment process for a given user ID.
- `continue_enrolment() -> (bool, int)`
  - Continues the enrollment process. Returns (success, progress).
- `cancel_enrollment(user_id) -> bool`
  - Cancels and erases the enrollment for a user ID.
- `get_total_enrolment_stages()`
  - Returns the number of stages in the enrollment process (usually 8).
- `is_enrolling()`
  - Returns True if enrollment is in progress.

### User Management

- `delete_all_users() -> bool`
  - Deletes all enrolled fingerprints.
- `delete_user(user_id) -> bool`
  - Deletes a specific user by ID.

### Information

- `get_firmware_version() -> int | None`
  - Gets the firmware version of the sensor.
- `get_firmware_release_date() -> datetime.date | None`
  - Gets the firmware release date.
- `get_sensor_type() -> int | None`
  - Gets the sensor type.
- `get_last_acknowledgement() -> int | None`
  - Gets the last acknowledgement code from the sensor.

### Low-Level Communication

- `send_command(command, param1=0, param2=0, param3=0, param4=0)`
  - Sends a raw command to the sensor (advanced usage).
- `read_response(length=8) -> bytes`
  - Reads a raw response from the sensor (advanced usage).

---

For more details and usage examples, see the [main documentation](overview.md).
