# GTNUCL1633 Fingerprint Reader
This repo contains a basic module for interacting with the GT-NUCL1633 Fingerprint Reader.

Currently supported features:
- Initialize (Open) Reader
- Terminate (Close) Reader
- Get unused user id (Used for training fingerprints)
- Switch LED On/Off

For any unimplemented features you can use `send_command` and `read_response` to fill the gaps.

## Additional Information
This is the very helpful programming guide if you are interested in contributing: https://cdn.sparkfun.com/assets/1/4/5/e/7/GT-NUCL1633K1_Programming_guide_V1.3.pdf