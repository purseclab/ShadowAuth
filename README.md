# ShadowAuth

This is the code repository for our ASIACCS'22 paper: [ShadowAuth: Backward-Compatible Automatic CAN Authentication for Legacy ECUs](https://dl.acm.org/doi/10.1145/3488932.3523263).

ShadowAuth is a packet authentication framework for a CAN bus.

You can freely use this repo to:

1. [figure out a CAN packet transmission function from ECU firmware](https://github.com/purseclab/ShadowAuth/tree/main/ecu_firmware_analysis),
2. [generate ARM Thumb machine codes designed for detour-based firmware instrumentation](https://github.com/purseclab/ShadowAuth/tree/main/ecu_firmware_rewriter), and
3. [build an ECU application for CAN packet authentication](https://github.com/purseclab/ShadowAuth/tree/main/authenticator)

Please see each README for further information.
