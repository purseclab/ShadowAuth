import matplotlib.pyplot as plt
import glob, os
import numpy as np
from operator import itemgetter, attrgetter
import re

ms3_path = 'ms3_pcode_last'
rusefi_path = 'rusefi_pcode'

path = ms3_path

branches = (
  "branch ",
  "cbranch ",
  "branchind ",
  "call ",
  "callind ",
  "return ",
)


def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)

def index_dispenser(startsfrom = 0):
  i = startsfrom;
  while True:
    yield i
    i += 1

def find_index_by_key(l, key, default=None):
  idx = 0
  for elem in l:
    if elem.key == key:
      return idx
    idx += 1
  return default

def find_index_by_addr(mmio_list, addr, default=None):
  idx = 0
  for elem in mmio_list:
    if elem.address == addr:
      return idx
    idx += 1
  return default

class MMIO:
  regex = "^\*\[ram\]unique\[0x([0-9a-z]+):[0-9]\] = (?:unique|register)\[0x[0-9a-z]+:([0-9])\]$"
  prog = re.compile(regex, flags = re.IGNORECASE | re.MULTILINE)
  index = index_dispenser()
  def __init__(self, addr, cnt=0, inb=0):
    self.key = next(MMIO.index)
    self.address = addr
    self.count = cnt
    self.inbound = inb
  
  def __str__(self):
    hexified = hex(row2_to_int(self.address))
    return f"""MMIO address: {hexified}
STR bytes: {self.inbound}"""

class BasicBlock:
  index = index_dispenser()
  def __init__(self, mmio):
    self.key = next(BasicBlock.index)
    self.mmio = mmio

def split_bb(content):
  res = ""
  for line in content.splitlines():
    res = f"{res}\n{line}"
    if line.startswith(branches):
      yield res
      res = ""
  yield res

def mmio_count(pcode):
  mmio_list = []
  for match in MMIO.prog.findall(pcode):
    mmio_idx = find_index_by_addr(mmio_list, match[0])
    if mmio_idx is None:
      mmio = MMIO(addr=match[0])
      # print(f"new addr: {match[0]}")
      mmio_list.append(mmio)
      mmio_idx = -1
    
    mmio_list[mmio_idx].count += 1
    mmio_list[mmio_idx].inbound += int(match[1])

    # if mmio_list[mmio_idx].address == "17820":
    #   print(mmio_list[mmio_idx])
    #   input("asdf")
    

  return mmio_list

def main():
  target_files = os.listdir(os.path.join(os.getcwd(), path))
  files_len = len(target_files)

  bbset = set()
  fset = set()
  aset = set()

  for filename in target_files:
    f = open(os.path.join(os.getcwd(), path,  filename), 'r')
    # f = open("rusefi_pcode/08026340.txt", 'r')
    # f = open("ms3_pcode_last/0000C301.txt", 'r')
    content = f.read()
    f.close()

    basic_blocks = split_bb(content)
    mmio_by_bb_list = []
    for bb in basic_blocks:
      mmio_by_bb_list.append(mmio_count(bb))

    mmio_by_func_list = mmio_count(content)

    idx = 0
    for i in mmio_by_bb_list:
      # print (f"== bb-{idx} ==")
      idx += 1
      for j in i:
        if j.inbound >= 8:
          # print(j, filename)
          bbset.add(filename)
          aset.add(j.address)
          # print(j)

    for i in mmio_by_func_list:
      if i.address not in aset:
        # input(aset)
        continue
      if i.inbound <= 12:
        fset.add(filename)
      # print(i)
    # input()
  print(bbset.intersection(fset))
  print(len(bbset.intersection(fset)))
  print("0000C301.txt" in bbset.intersection(fset))
  print("08026340.txt" in bbset.intersection(fset))

if __name__ == "__main__":
  main()



"""
rusefi: 114b0, top 8, 24, bot: 32
ms3: 1080, top 16, 6, 10, bot: 32
bb_mmio_cnt = [
  {
    bb_key: 1, # unique for bb
    mmio: {
      address: 0x1234,
      count: 3,
      inbound: 3, # byte
    }
  },
  { ... }
  ...
]

func_mmio_cnt = [
  {
    address: 0x1234,
    count: 3,
    inbound: 4, # byte
  },
  { ... },
  ...
]
"""
