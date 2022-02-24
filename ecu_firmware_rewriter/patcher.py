from src.ArmUtils import ArmUtils
import os


load_at = 0x08000000
CAN_TRANSMIT_TIMEOUT = 0x08048d90
CAN_DRIVER = 0x200025e8
ECUID=0x12345678
NONCE=0xabcdef

rewriting_point = 0x802aa40 + 54 #0x802aa74
rewriting_point_offset = rewriting_point - load_at

func_size = 144
func_address = 0x130

PSTACK_END=0x2000FBA6
# PSTACK_END=0x10004E2C



def gen_detour(from_offset, func_offset, detour_offset):
    pc = detour_offset
    to_offset = detour_offset

    alt = ArmUtils.jump(detour_offset - from_offset)

    save = f_rusefi[from_offset:from_offset+2]
    if ArmUtils.is_2byte(save) is True:
        target2 = f_rusefi[from_offset+2:from_offset+4]
        if ArmUtils.is_2byte(target2) is True:
            save += target2
        else:
            save = f_rusefi[from_offset:from_offset+6]
            alt += ArmUtils.nop

    detour_code = save
    pc += len(save)

    high = PSTACK_END >> 16
    low = PSTACK_END & 0xFFFF    
    
    detour_code += ArmUtils.mov(1, low)
    pc += 4
    detour_code += ArmUtils.movt(1, high)
    pc += 4
    detour_code += ArmUtils.store(ArmUtils.SP, 1, 0)
    pc += 4
    
    detour_code += ArmUtils.mov(ArmUtils.SP, low)
    pc += 4
    detour_code += ArmUtils.movt(ArmUtils.SP, high)
    pc += 4

    detour_code += ArmUtils.call(func_offset - pc)
    pc += 4
    
    detour_code += ArmUtils.mov(1, low)
    pc += 4
    detour_code += ArmUtils.movt(1, high)
    pc += 4
    detour_code += ArmUtils.load(ArmUtils.SP, 1, 0)
    pc += 4

    print(hex(pc))
    detour_code += ArmUtils.jump_back(pc - from_offset - len(alt))
    pc += 4   

    return alt, detour_code


ecuid_high = ECUID >> 16
ecuid_low = ECUID & 0xFFFF
nonce_high = NONCE >> 16
nonce_low = NONCE & 0xFFFF
f_global = ecuid_high.to_bytes(2, 'little') + \
    ecuid_low.to_bytes(2, 'little') + \
    nonce_high.to_bytes(2, 'little') + \
    nonce_low.to_bytes(2, 'little')



rusefi_bin = open('rusefi.bin', 'rb')
f_rusefi = rusefi_bin.read()
rusefi_bin.close()



detourcode_bin = open('c/detourcode.bin', 'rb')
f_detourcode = detourcode_bin.read()
detourcode_bin.close()


contents = f_rusefi + f_detourcode + f_global
func_offset = len(f_rusefi) + func_address

print("ECUID Address: ", hex(load_at + len(contents)))


alt, detour_code = gen_detour(rewriting_point_offset, func_offset, len(contents))
contents = ArmUtils.insert_bytes(contents, rewriting_point_offset, alt)
contents += detour_code

with open('patched.bin', 'wb') as f:
    f.write(contents)

os.system("cp patched.bin /mnt/c/Users/swkim/Documents/patched.bin")


# patch(0x333, )