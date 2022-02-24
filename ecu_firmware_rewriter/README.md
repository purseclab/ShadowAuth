# ECU Firmware Rewriting Tool

## Setup

(Optional)
* arm-none-eabi-gcc
* arm-none-eabi-objcopy

## Usage

[ArmUtils.py](https://github.com/purseclab/ShadowAuth/blob/main/ecu_firmware_rewriter/src/ArmUtils.py)
has various static and independent functions to help detour-based rewriting.  
It supports well-known technical features, such as `move`, `store`, `load`, forward and backward `jump` and `call`, and instruction length detection.

[patcher.py](https://github.com/purseclab/ShadowAuth/blob/main/ecu_firmware_rewriter/patcher.py) includes an use-case of those functions as follows:

```python
detour_inst = ArmUtils.jump(detour_offset - from_offset)
saved_inst1 = firmware[from_offset:from_offset+2]
# since detour_inst is 4 byte, 
if ArmUtils.is_2byte(saved_inst1) is True:
    saved_inst2 = firmware[from_offset+2:from_offset+4]
    if ArmUtils.is_2byte(saved_inst2) is True:
        saved_inst1 += saved_inst2
    else:
        saved_inst1 = firmware[from_offset:from_offset+6]
        detour_inst += ArmUtils.nop

trampoline_code = saved_inst1
pc += len(saved_inst1)

high = PSTACK_END >> 16
low = PSTACK_END & 0xFFFF    

# save registers
trampoline_code += ArmUtils.mov(1, low)
pc += 4
trampoline_code += ArmUtils.movt(1, high)
pc += 4
trampoline_code += ArmUtils.store(ArmUtils.SP, 1, 0)
pc += 4
trampoline_code += ArmUtils.mov(ArmUtils.SP, low)
pc += 4
trampoline_code += ArmUtils.movt(ArmUtils.SP, high)
pc += 4

# run desired function
trampoline_code += ArmUtils.call(func_offset - pc)
pc += 4

# recover registers
trampoline_code += ArmUtils.mov(1, low)
pc += 4
trampoline_code += ArmUtils.movt(1, high)
pc += 4
trampoline_code += ArmUtils.load(ArmUtils.SP, 1, 0)
pc += 4

# go back to the original control flow
trampoline_code += ArmUtils.jump_back(pc - detour_inst))
```