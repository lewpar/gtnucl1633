# GTNUCL1633 Fingerprint Reader
A Python module implementation of the GTNUCL1633 Fingerprint Reader.

## Usage
Checkout [main.py](./main.py) for basic usage.

## Supported Commands
- [x] CMD_OPEN
- [x] CMD_CLOSE
- [x] CMD_LED_CONTROL
- [x] CMD_IS_PRESS_FINGER
- [ ] CMD_ENROLL
- [ ] CMD_DELETE_ID
- [ ] CMD_DELETE_ALL
- [ ] CMD_GET_USER_COUNT
- [ ] CMD_IDENTIFY
- [x] CMD_GET_ENTRY_ID
- [ ] CMD_GET_FIRMWARE_VERSION
- [ ] CMD_ENROLL_CANCEL

For any unimplemented features you can use `send_command` and `read_response` to fill the gaps.

## Additional Information
This is the very helpful programming guide if you are interested in contributing: https://cdn.sparkfun.com/assets/1/4/5/e/7/GT-NUCL1633K1_Programming_guide_V1.3.pdf