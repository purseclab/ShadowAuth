from src.POJO import EngineControlUnit
from src.POJO import Context
from src import HashContextMap
import asyncio
import json
import can
from blake3 import blake3
import datetime

can_ecu_map = {}
__DEBUG__ = True

def log(*argv, end="\n"):
    if __DEBUG__ == True:
        print(*argv, end=end)


def hash(ecuid: int, nonce: int, canid: bytes) -> bytes:
    hasher = blake3.blake3_hasher_init()

    blake3.blake3_hasher_update(hasher, canid, 4)

    blake3.blake3_hasher_update(hasher, ecuid, 4)

    blake3.blake3_hasher_update(hasher, nonce, 4)

    hashed = blake3.blake3_hasher_finalize(hasher, 8)
    return hashed


def print_bytes(b):
    for i in b:
        log(hex(i), end=' ')
    log()

async def handle_plain_msg(ctx: Context.Context) -> None:
    hashContextMap = HashContextMap.HashContextMap.getInstance()
    log('[plain] ', hex(ctx.can_id))
    log('[plain] ', ctx.msg)
    ecus = can_ecu_map.get(ctx.can_id, [])
    hashes = []
    for e in ecus:
        hashed = hash(e.id, e.nonce, ctx.can_id)
        log('[expect] ', end='')
        print_bytes(hashed)
        hashContextMap[hashed] = (ctx, e)
        hashes.append(hashed)

    await asyncio.sleep(0.01)

    if ctx.is_authenticated is True:
        log('Authenticated!, can_id: ', hex(ctx.can_id), ' ecu_id: ', hex(ctx.ecu.id))
    else:
        log('DANGER! WE ARE UNDER ATTACK!, can_id: ', hex(ctx.can_id))
    for h in hashes:
        if hashContextMap.get(h, None) is not None:
            del hashContextMap[h]

async def handle_auth_msg(ctx: Context.Context)  -> None:
    hashContextMap = HashContextMap.HashContextMap.getInstance()
    plain_ctx, ecu = hashContextMap.get(ctx.msg, (None, None))
    log('[auth] ', end='')
    print_bytes(ctx.msg)
    if plain_ctx is not None:
        ecu.increase_nonce()
        plain_ctx.is_authenticated = True
        plain_ctx.ecu = ecu

async def handler(ctx: Context.Context):
    if ctx.can_id == 0x212:
        return
    if ctx.can_id == 0x201:
        return
    if ctx.can_id == 0x420:
        return
    if ctx.can_id == 0x1ff:
        await handle_auth_msg(ctx)
    else:
        await handle_plain_msg(ctx)

async def main():
    with open('can_ecu_map.json', "r") as f: 
        _can_ecu_map = json.loads(f.read())
        for k in _can_ecu_map.keys():
            if can_ecu_map.get(int(k), None) is None:
                can_ecu_map[int(k)] = []
            for i in _can_ecu_map[k]:
                can_ecu_map[int(k)].append(EngineControlUnit.EngineControlUnit(id=i["id"]))
        log(can_ecu_map)
    tasks = []
    can_interface = 'can0'
    bus = can.interface.Bus(can_interface, bustype='socketcan_native')
    i = 0
    while i < 200:
        message = bus.recv(1.0) # Timeout in seconds.
        await asyncio.sleep(0.001)
        if message is None:
            log('Timeout occurred, no message.')
            continue
        canid = message.arbitration_id
        log("canid (int): ", hex(message.arbitration_id))
        data = bytes(message.data)
        ctx = Context.Context(can_id=canid, msg=data)
        if canid == 0x300:
            i += 1
        print(i, " / 200")
        asyncio.create_task(handler(ctx))

asyncio.run(main())
exp.close()
