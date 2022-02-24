TARGET = libblake3
#CC=arm-none-eabi-gcc
CC=gcc
CFLAGS = -g -Wall -O3 -fPIC -shared
CFLAGS += -DBLAKE3_NO_SSE2 -DBLAKE3_NO_SSE41 -DBLAKE3_NO_AVX2 -DBLAKE3_NO_AVX512
#CFLAGS += -mlittle-endian -mthumb -mcpu=cortex-m4 -mthumb-interwork
#CFLAGS += -mfloat-abi=hard -mfpu=fpv4-sp-d16
#CFLAGS += --specs=nosys.specs

OBJS = blake3.o blake3_dispatch.o blake3_portable.o
SRCS = blake3.c blake3_dispatch.c blake3_portable.c

#AR = arm-none-eabi-ar
AR = ar
ARFLAGS = -rcs

all: $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET).so $(OBJS)
	$(AR) $(ARFLAGS) $(TARGET).a $(OBJS)

clean:
	rm -f *.o $(TARGET).a
	rm -f $(TARGET).so
