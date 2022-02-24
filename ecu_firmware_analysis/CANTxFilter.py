import os
import re
import math

REGEX = "\*\[ram\]unique\[0x([0-9a-z]+):[0-9]\] = (?:unique|register)\[0x[0-9a-z]+:([0-9])\]$"
prog = re.compile(REGEX, re.IGNORECASE)

def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)


x = []
y = []

xy = []


ms3_path = 'ms3_pcode'
ms3_ans = 0xc301
rusefi_path = 'rusefi_pcode'
rusefi_ans = 0x8026340
sty_path = 'sty_pcode'
sty_ans = 0x8002b34




branches = (
  "branch ",
  "cbranch ",
  "branchind ",
  "call ",
  "callind ",
  "return ",
)


def main():
  ## input
  ans = ms3_ans
  path = ms3_path
  ##
  all = len(os.listdir(os.path.join(os.getcwd(), path)))
  cur = 1
  value = 0
  true_positive = False
  bb_rawdata = open(f"{path}_basicblock_str_distribution.txt", "w")
  func_rawdata = open(f"{path}_fucntion_str_distribution.txt", "w")
  for filename in os.listdir(os.path.join(os.getcwd(), path)):
    func_addr = row2_to_int(filename.split(".")[0])
    file_path = os.path.join(os.getcwd(), path,  filename)
    bb_mmio_cnt = run(file_path, func_addr)

    mmio_cnt = aggregate_by_mmio_id(bb_mmio_cnt)

    (bbmin, bbmax) = minmax_bb_mmio_cnt(bb_mmio_cnt, 63)
    (mmiomin, mmiomax) = minmax_mmiocnt(mmio_cnt, 92)

    save_by_bb(bb_mmio_cnt, bb_rawdata)
    save_by_func(mmio_cnt, func_rawdata)    

    # print(f"{cur}/{all}")
    cur += 1

    if bbmax >= 8 and mmiomax >= 10:
      value += 1
      # print(hex(func_addr))
      if func_addr == ans:
        true_positive = True

  bb_rawdata.close()
  func_rawdata.close()

  print(f"{value}/{all}")
  print(true_positive)

def minmax_bb_mmio_cnt(bb_mmio_cnt, n):
  min = math.inf
  max = 0
  bb_ids = bb_mmio_cnt.keys()
  for bb_id in bb_ids:
    mmio_addrs = bb_mmio_cnt[bb_id].keys()
    for mmio_addr in mmio_addrs:
      cnt = bb_mmio_cnt[bb_id][mmio_addr]
      min = cnt if cnt < min else min
      max = cnt if cnt > max else max
      
  return (min, max)


def minmax_mmiocnt(mmio_cnt, n):
  min = math.inf
  max = 0
  mmio_addrs = mmio_cnt.keys()
  for addr in mmio_addrs:
    cnt = mmio_cnt[addr]
    min = cnt if cnt < min else min
    max = cnt if cnt > max else max
  return (min, max)


def aggregate_by_mmio_id(bb_mmio_cnt):
  mmio_cnt = {}
  bb_ids = bb_mmio_cnt.keys()
  for bb_id in bb_ids:
    bb_mmio_addrs = bb_mmio_cnt[bb_id].keys()
    for bb_mmio_addr in bb_mmio_addrs:
      mmio_cnt[bb_mmio_addr] = mmio_cnt.get(bb_mmio_addr, 0) + bb_mmio_cnt[bb_id][bb_mmio_addr]

  return mmio_cnt

def save_by_bb(bb_mmio_cnt, f):
  bb_ids = bb_mmio_cnt.keys()
  for bb_id in bb_ids:
    mmio_addrs = bb_mmio_cnt[bb_id].keys()
    for mmio_addr in mmio_addrs:
      a = hex(row2_to_int(mmio_addr))
      f.write(f"{bb_mmio_cnt[bb_id][mmio_addr]}\n")

def save_by_func(mmio_cnt, f):
  mmio_addrs = mmio_cnt.keys()
  for addr in mmio_addrs:
    cnt = mmio_cnt[addr]
    f.write(f"{cnt}\n")
    

def print_by_bb(bb_mmio_cnt):
  '''
  function_id: {
    basic_block_ids: {
      mmio_addrs: cnt
    }
  }

  get_cnt_by_mmio(mmio_addr)
  '''
  bb_ids = bb_mmio_cnt.keys()
  for bb_id in bb_ids:
    print(f"bb: {bb_id}")
    mmio_addrs = bb_mmio_cnt[bb_id].keys()
    for mmio_addr in mmio_addrs:
      a = hex(row2_to_int(mmio_addr))
      print(f"  {a}: {bb_mmio_cnt[bb_id][mmio_addr]}")






def is_mmio_instr(pcode):
  m = prog.match(pcode)
  return m is not None

# returns (ok, mmio_addr, mmio_cnt)
def parse_mmio_cnt(pcode):
  if is_mmio_instr(pcode) is False:
    return (False, None, None)
  m = prog.match(pcode)
  g = m.groups()

  if len(g) <= 1:
    return (False, None, None)
  
  mmio_addr = g[0]
  mmio_cnt = int(g[1])

  return (True, mmio_addr, mmio_cnt)

def is_branch_instr(pcode):
  return pcode.lower().startswith(branches)

def run(file_path, func_addr):
  mmio_cnt = {}
  current_bb_id = 0 #current basic_block id, incrementlal thing
  mmio_cnt[current_bb_id] = {}
  with open(file_path, 'r') as f:
    for line in f:
      # check the given line is branch instr
      is_branch = is_branch_instr(line)
      if is_branch is True:
        current_bb_id += 1
        mmio_cnt[current_bb_id] = {}
        continue

      # parse the given line as mmio instr
      (is_mmio, addr, cnt) = parse_mmio_cnt(line)
      if is_mmio is False:
        continue

      mmio_cnt[current_bb_id][addr] = mmio_cnt[current_bb_id].get(addr, 0) + cnt
  
  return mmio_cnt
      

if __name__ == "__main__":
  main()




"""
func: 0x8002b34
  bbmin: 1
  bbmax: 40
  mmiomin: 13
  mmiomax: 76

func: 0xc301
  bbmin: 1
  bbmax: 16
  mmiomin: 1
  mmiomax: 36

func: 0x8026340
  bbmin: 4
  bbmax: 24
  mmiomin: 8
  mmiomax: 36
"""