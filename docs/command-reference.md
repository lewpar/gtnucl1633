# GTNUCL1633 Command & Acknowledgement Reference

This page lists the command and acknowledgement constants used by the GTNUCL1633 fingerprint sensor.

## Command Constants

| Constant | Value | Description |
|----------|-------|-------------|
| CMD_OPEN | 0xA0 | Initialize the fingerprint module |
| CMD_CLOSE | 0xA1 | Terminate the fingerprint module |
| CMD_LED_CONTROL | 0xB4 | Control the sensor LED |
| CMD_IS_PRESS_FINGER | 0xB5 | Check if a finger is on the sensor |
| CMD_ENROLL | 0x01 | Start fingerprint enrollment |
| CMD_DELETE_ID | 0x04 | Delete fingerprint by ID |
| CMD_DELETE_ALL | 0x05 | Delete all fingerprints |
| CMD_GET_USER_COUNT | 0x09 | Get number of enrolled fingerprints |
| CMD_IDENTIFY | 0x0C | Identify fingerprint (1:N) |
| CMD_GET_ENTRY_ID | 0x0D | Get unused fingerprint ID |
| CMD_GET_FIRMWARE_VERSION | 0x26 | Get firmware version |
| CMD_ENROLL_CANCEL | 0x92 | Cancel enrollment |
| CMD_UART_CONTROL | 0xA3 | Control UART baud rate |

### UART Baud Rate Values
| Constant | Value | Description |
|----------|-------|-------------|
| CMD_UART_CONTROL_BAUD_9600 | 0x1 | 9600 baud |
| CMD_UART_CONTROL_BAUD_19200 | 0x2 | 19200 baud |
| CMD_UART_CONTROL_BAUD_115200 | 0x3 | 115200 baud |
| CMD_UART_CONTROL_BAUD_230400 | 0x4 | 230400 baud |
| CMD_UART_CONTROL_BAUD_460800 | 0x5 | 460800 baud |
| CMD_UART_CONTROL_BAUD_921600 | 0x6 | 921600 baud |

## Acknowledgement Codes

| Constant | Value | Description |
|----------|-------|-------------|
| ACK_SUCCESS | 0x00 | Command executed successfully |
| ACK_FAIL | 0x01 | Command execution failed |
| ACK_FULL | 0x04 | Fingerprint database is full |
| ACK_NOUSER | 0x05 | ID not registered |
| ACK_USER_EXIST | 0x07 | ID already registered |
| ACK_TIMEOUT | 0x08 | Timeout while capturing finger |
| ACK_WRONG_FORMAT | 0x09 | Wrong fingerprint template format |
| ACK_BREAK | 0x18 | Command was aborted |
| ACK_INVALID_PARAMETER | 0xB0 | Invalid parameter |
| ACK_FINGER_IS_NOT_PRESSED | 0xB1 | No finger on sensor |
| ACK_COMMAND_NO_SUPPORT | 0xB4 | Command not supported |
| ACK_ENROLL_OVEREXPOSURE | 0xB5 | Overexposed image during enrollment |
| ACK_ENROLL_MOVE_MORE | 0xB6 | Finger moved too little during enrollment |
| ACK_ENROLL_MOVE_LESS | 0xB7 | Finger moved too much during enrollment |
| ACK_ENROLL_DUPLICATE | 0xB8 | Duplicate finger position detected |
| ACK_FINGER_PRESS_NOT_FULL | 0xB9 | Finger not fully pressed |
| ACK_ENROLL_POOR_QUALITY | 0xBA | Poor image quality during enrollment |

---

For more details, see the [API Reference](api-reference.md) or the [main documentation](overview.md).
