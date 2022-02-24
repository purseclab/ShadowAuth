#include "blake3.h"

#define CH_CFG_ST_FREQUENCY     148000000 //148Mhz
#define CAN_IDE_STD             0
#define CAN_IDE_EXT             1 
#define CAN_RTR_DATA            0
#define CAN_RTR_REMOTE          1

#define TIME_MS2I(msecs)                                                    \
  ((int)((((int)(msecs) *                                 \
                     (int)CH_CFG_ST_FREQUENCY) +                    \
                    (int)999) / (int)1000))

typedef struct {
  struct {
    uint8_t                 DLC:4;          /**< @brief Data length.        */
    uint8_t                 RTR:1;          /**< @brief Frame type.         */
    uint8_t                 IDE:1;          /**< @brief Identifier type.    */
  };
  union {
    struct {
      uint32_t              SID:11;         /**< @brief Standard identifier.*/
    };
    struct {
      uint32_t              EID:29;         /**< @brief Extended identifier.*/
    };
  };
  union {
    uint8_t                 data8[8];       /**< @brief Frame data.         */
    uint16_t                data16[4];      /**< @brief Frame data.         */
    uint32_t                data32[2];      /**< @brief Frame data.         */
    uint64_t                data64[1];      /**< @brief Frame data.         */
  };
} CANTxFrame;

void __attribute__((noinline)) second_message() {
    void (*canTransmitTimeout)
      (void*, uint32_t, CANTxFrame*, uint32_t)
      = CAN_TRANSMIT_TIMEOUT;
    void* a1 = CAN_DRIVER;
    uint32_t *ecuid = ECUID;
    // uint32_t *nonce = NONCE;
    // uint32_t *counter = 0xdddddddd; // .ram
    uint8_t out[8];

    {
      blake3_hasher a;
      blake3_hasher_init(&a);
      blake3_hasher_update(&a, ecuid, sizeof(uint32_t));
      // blake3_hasher_update(&a, nonce, sizeof(uint32_t));
      // blake3_hasher_update(&a, counter, sizeof(uint32_t));
      blake3_hasher_finalize(&a, out, 8);
    }

    CANTxFrame frame;
    frame.IDE = CAN_IDE_EXT;
    frame.EID = 0x1dd;
    frame.RTR = CAN_RTR_DATA;
    frame.DLC = 8;

    canTransmitTimeout(a1, 0, &frame, TIME_MS2I(100));
}


int main() {
    return 0;
}