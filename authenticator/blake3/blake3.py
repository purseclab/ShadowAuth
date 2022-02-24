from ctypes import *

'''
#define BLAKE3_VERSION_STRING "0.3.7"
#define BLAKE3_KEY_LEN 32
#define BLAKE3_OUT_LEN 8
#define BLAKE3_BLOCK_LEN 8
#define BLAKE3_CHUNK_LEN 32
#define BLAKE3_MAX_DEPTH 4
#define BLAKE3_MAX_SIMD_DEGREE 16

typedef struct {
  uint32_t cv[8];
  uint64_t chunk_counter;
  uint8_t buf[BLAKE3_BLOCK_LEN];
  uint8_t buf_len;
  uint8_t blocks_compressed;
  uint8_t flags;
} blake3_chunk_state;

typedef struct {
  uint32_t key[8];
  blake3_chunk_state chunk;
  uint8_t cv_stack_len;
  uint8_t cv_stack[(BLAKE3_MAX_DEPTH + 1) * BLAKE3_OUT_LEN];
} blake3_hasher;
'''
BLAKE3_VERSION_STRING="0.3.7"
BLAKE3_KEY_LEN=32
BLAKE3_OUT_LEN=8
BLAKE3_BLOCK_LEN=8
BLAKE3_CHUNK_LEN=32
BLAKE3_MAX_DEPTH=4
BLAKE3_MAX_SIMD_DEGREE=16

class blake3_chunk_stack(Structure):
    _fields_ = [("cv", c_uint * 8),
                ("chunk_counter", c_ulonglong),
                ("buf", c_ubyte * BLAKE3_BLOCK_LEN),
                ("buf_len", c_ubyte),
                ("blocks_compressed", c_ubyte),
                ("flags", c_ubyte)]

class blake3_hasher(Structure):
	_fields_ = [("key", c_uint * 8),
                ("chunk", blake3_chunk_stack),
                ("cv_stack_len", c_ubyte),
                ("cv_stack", c_ubyte * (BLAKE3_MAX_DEPTH + 1) * BLAKE3_OUT_LEN),]

blake3 = CDLL("./blake3/libblake3.so")

def blake3_hasher_init():
    instance = blake3_hasher()
    blake3.blake3_hasher_init(byref(instance))
    return instance

def blake3_hasher_update(self, value, length):
    a = []
    for i in value.to_bytes(length, 'little'):
        a.append(i)
    value = (c_byte * length)(*a)
    blake3.blake3_hasher_update(byref(self), byref(value), length)
    return self

def blake3_hasher_finalize(self, length):
    value = c_ulonglong()
    blake3.blake3_hasher_finalize(byref(self), byref(value), length)
    return value.value.to_bytes(length, 'little')

if __name__ == "__main__":
    a = blake3_hasher_init()
    blake3_hasher_update(a, 0x300, 4)
    blake3_hasher_update(a, 0xdeadbeef, 4)
    res = blake3_hasher_finalize(a, 8)
    for i in range(8):
        print(hex(res[i]), end=' ')
    print()
