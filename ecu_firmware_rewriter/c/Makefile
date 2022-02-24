TARGET = detourcode
CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy
CFLAGS = -g -Wall -O0 -fPIC -static
CFLAGS += -D'CAN_TRANSMIT_TIMEOUT=0x08048d90'
CFLAGS += -D'CAN_DRIVER=0x200025e8'
CFLAGS += -D'ECUID=0x809fac4'
# CFLAGS += -D'NONCE=0xdddd'
CFLAGS += -DBLAKE3_NO_SSE2 -DBLAKE3_NO_SSE41 -DBLAKE3_NO_AVX2 -DBLAKE3_NO_AVX512
CFLAGS += -mlittle-endian -mthumb -mcpu=cortex-m4 -mthumb-interwork
CFLAGS += -mfloat-abi=hard -mfpu=fpv4-sp-d16
CFLAGS += --specs=nosys.specs
CFLAGS += -I./blake3

OBJS = main.o blake3/blake3.o blake3/blake3_dispatch.o blake3/blake3_portable.o
SRCS = main.c blake3.c blake3_dispatch.c blake3_portable.c

all: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET).elf
	$(OBJCOPY) -O binary $(TARGET).elf $(TARGET).bin
	cp $(TARGET).elf /mnt/c/Users/swkim/Documents/$(TARGET).elf
	cp $(TARGET).bin /mnt/c/Users/swkim/Documents/$(TARGET).bin

clean:
	rm -f *.o $(TARGET).elf
	rm -f *.o $(TARGET).bin
