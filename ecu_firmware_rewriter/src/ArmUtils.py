import os 

'''
In these instructions:
L: specifies whether the instruction is a load (L == 1) or a store (L == 0)
S: specifies whether a load is sign extended (S == 1) or zero extended (S == 0)
U: specifies whether the indexing is upwards (U == 1) or downwards (U == 0)
Rn: cannot be r15 (if it is, the instruction is PC +/- imm12)
Rm: cannot be r13 or r15 (if it is, the instruction is UNPREDICTABLE)
'''

def print_bin(e):
    for i in e:
        print(hex(i), end=' ')
    print('')

class ArmUtils:
    CC = "arm-none-eabi-gcc"
    CC_O = " -c"
    OBJCOPY = "arm-none-eabi-objcopy"
    OBJCOPY_O = " -O binary"

    SP = 0xD

    @staticmethod
    def assemble(code: str) -> bytearray:
        """
        Takes assembly code, returns assembled binary.
        """
        res = b""
        with open("tmp.s", "w") as f:
            f.write(str(code))
        os.system(ArmUtils.CC + ArmUtils.CC_O + " tmp.s")
        os.system(ArmUtils.OBJCOPY + ArmUtils.OBJCOPY_O + " tmp.o" + " tmp.bin")
        with open("tmp.bin", "rb") as f:
            res = f.read()
        return res

    @staticmethod
    def is_4byte(opcode: bytes) -> bool:
        """
        Takes an opcode, returns true if it is 4-byte length opcode
        """
        low, high = opcode # little-endian
        if (high & 0b11110000) == 0b11110000:
            return True
        if (high & 0b11101000) == 0b11101000:            
            return True
        return False

    @staticmethod
    def is_2byte(opcode: bytes) -> bool:
        """
        Takes an opcode, returns true if it is 2-byte length opcode
        """
        return (not ArmUtils.is_4byte(opcode))

    @staticmethod
    def jump(size: int) -> bytearray:
        """
        Takes pre-calculated PC-relative length, returns a forward jump instruction
        15                        0 15                        0
        1111 0S[ I M M 1 0        ] 10[J1]1 [J2][ I M M 1 1   ]
        1111 00[ I M M 1 0        ] 1011    1[  I  M  M  1  1 ]
        I = NOT(J EOR S)
        S:I1:I2:imm10:imm11:'0'
        """
        if size < 0:
            return ArmUtils.jump_back(-size)
        size = size - 4
        size = size >> 1
        imm10 = (size & 0b111111111100000000000) >> 11
        imm11 = size & 0b11111111111
        high = (0b111100 << 10) | imm10
        low = (0b10111 << 11) | imm11
        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little') 

    @staticmethod
    def jump_back(size: int) -> bytearray:
        """
        Takes pre-calculated PC-relative length, returns a forward jump instruction
        15                        0 15                        0
        1111 0S[ I M M 1 0        ] 10[J1]1 [J2][ I M M 1 1   ]
        1111 00[ I M M 1 0        ] 1011    1[  I  M  M  1  1 ]
        I = NOT(J EOR S)
        S:I1:I2:imm10:imm11:'0'
        """
        size = size + 4
        size = (size ^ 0xFFFFFFFF) + 1
        size = size >> 1
        imm10 = (size & 0b111111111100000000000) >> 11
        imm11 = size & 0b11111111111
        high = (0b111101 << 10) | imm10
        low = (0b10111 << 11) | imm11
        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little')

    @staticmethod
    def call(size: int) -> bytearray:
        """
        Takes pre-calculated PC-relative length, returns a forward jump instruction
        15                        0 15                           0
        1111 0S[ I M M 1 0        ] 11[J1]1 [J2][  I  M  M  1  1 ]
        1111 00[ I M M 1 0        ] 1111    1[  I  M  M  1  1 ]
        I = NOT(J EOR S)
        S:I1:I2:imm10:imm11:'0'
        """
        if size < 0:
            return ArmUtils.call_back(-size)
        size = size - 4
        size = size >> 1
        imm10 = (size & 0b111111111100000000000) >> 11
        imm11 = size & 0b11111111111
        high = (0b111100 << 10) | imm10
        low = (0b11111 << 11) | imm11
        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little')

    @staticmethod
    def call_back(size: int) -> bytearray:
        """
        Takes pre-calculated PC-relative length, returns a forward jump instruction
        15                        0 15                        0
        1111 0S[ I M M 1 0        ] 11[J1]1 [J2][ I M M 1 1   ]
        1111 00[ I M M 1 0        ] 1111    1[  I  M  M  1  1 ]
        I = NOT(J EOR S)
        S:I1:I2:imm10:imm11:'0'
        """
        size = size + 4
        size = (size ^ 0xFFFFFFFF) + 1
        size = size >> 1
        imm10 = (size & 0b111111111100000000000) >> 11
        imm11 = size & 0b11111111111
        high = (0b111101 << 10) | imm10
        low = (0b11111 << 11) | imm11
        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little')

    @property
    @staticmethod
    def nop() -> bytearray:
        """
        15                0
        1011 1111 0000 0000
        """
        return b'\x00\xBF'

    @staticmethod
    def insert_bytes(target: bytearray, offset: int, code: bytearray) -> bytearray:
        """
        Inserts 'code' into 'target' at 'offeset', returns it
        """
        b = bytearray(target)
        c = b[:offset] + code + b[offset + len(code):]
        return c

    @staticmethod
    def mov(r: int, imm16):
        """
        MOV
        15                  0 15                       0
        1111 0i10 0100 [imm4] 0[imm3] [ Rd ] [ i m m 8 ]
        imm4:i:imm3:imm8
        """
        imm4 = imm16 >> 12
        i = (imm16 >> 11) & 1
        imm3 = (imm16 >> 8) & 0b111
        imm8 = imm16 & 0b11111111

        high = 0b1111001001000000
        high = high | (i << 10)
        high = high | imm4

        low = imm3 << 12
        low = low | (r << 8)
        low = low | imm8
        
        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little')

    @staticmethod
    def movt(r: int, imm16):
        """
        MOVT
        15                  0 15                       0
        1111 0i10 1100 [imm4] 0[imm3] [ Rd ] [ i m m 8 ]
        imm4:i:imm3:imm8
        """
        imm4 = imm16 >> 12
        i = (imm16 >> 11) & 1
        imm3 = (imm16 >> 8) & 0b111
        imm8 = imm16 & 0b11111111

        high = 0b1111001011000000
        high = high | (i << 10)
        high = high | imm4

        low = imm3 << 12
        low = low | (r << 8)
        low = low | imm8
        
        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little')

    @staticmethod
    def store(rt, rn, imm12):
        """
        STR
        15                  0 15                0
        1111 1000 1100 [ Rn ] [ Rt ] [ i m m 12 ]
        Rt = Rn + imm12
        """

        if imm12 < 0:
            imm12 = -imm12
            imm12 = (imm12 ^ 0b111111111111) + 1

        high = 0b1111100011000000
        high = high | rn
        low = imm12
        low = low | (rt << 12)

        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little')

    @staticmethod
    def load(rt, rn, imm12):
        """
        LDR
        15                  0 15                0
        1111 1000 1101 [ Rn ] [ Rt ] [ i m m 12 ]
        Rt = Rn + imm12
        """
        if imm12 < 0:
            imm12 = -imm12
            imm12 = (imm12 ^ 0b111111111111) + 1

        high = 0b1111100011010000
        high = high | rn
        low = imm12
        low = low | (rt << 12)

        return high.to_bytes(2, 'little') + low.to_bytes(2, 'little')



