# GTNUCL1633 Fingerprint Reader
A Python module implementation of the GTNUCL1633 Fingerprint Reader.

## Usage
Checkout [main.py](./main.py) for basic usage.

## Supported Commands
- [x] CMD_OPEN
- [x] CMD_CLOSE
- [x] CMD_LED_CONTROL
- [x] CMD_IS_PRESS_FINGER
- [x] CMD_ENROLL
- [x] CMD_DELETE_ID
- [x] CMD_DELETE_ALL
- [x] CMD_GET_USER_COUNT
- [x] CMD_IDENTIFY
- [x] CMD_GET_ENTRY_ID
- [x] CMD_GET_FIRMWARE_VERSION
- [x] CMD_ENROLL_CANCEL
- [x] CMD_UART_CONTROL

For any unimplemented features you can use `send_command` and `read_response` to fill the gaps.

## Additional Information
This is the very helpful programming guide if you are interested in contributing: https://cdn.sparkfun.com/assets/1/4/5/e/7/GT-NUCL1633K1_Programming_guide_V1.3.pdf

Datasheet: https://cdn.sparkfun.com/assets/0/4/f/d/9/GT-nucl1633k1_product_specification_v1.2_20220509.pdf