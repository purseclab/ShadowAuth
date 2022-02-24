import matplotlib.pyplot as plt
import glob, os
import numpy as np
from operator import itemgetter, attrgetter
import re

REGEX = "^\*\[ram\]unique\[0x([0-9a-z]+):[0-9]\] = (?:unique|register)\[0x[0-9a-z]+:([0-9])\]$"
prog = re.compile(REGEX, re.IGNORECASE)

def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)


x = []
y = []

xy = []


ms3_path = 'ms3_pcode_last'
rusefi_path = 'rusefi_pcode'

path = rusefi_path

branches = (
  "branch ",
  "cbranch ",
  "branchind ",
  "call ",
  "callind ",
  "return ",
)

all = len(os.listdir(os.path.join(os.getcwd(), path)))
cur = 1
cred_cnt = 0
bb_cnt = 0
func_cnt = 0
for filename in os.listdir(os.path.join(os.getcwd(), path)):
  mmiobyte = 0
  # print(f"{cur}/{all}")
  cur += 1
  j = 0
  jz = {}
  bb = {}
  with open(os.path.join(os.getcwd(), path,  filename), 'r') as f: # open in readonly mode
    h = row2_to_int(filename.split(".")[0])
    for line in f:
      m = prog.match(line)
      if m is None:
        if line.lower().startswith(branches):
          for jz_key in jz:
            if jz[jz_key] < 26:
              # cred_cnt += 1
              cred_cnt = cred_cnt + 1 if j == 0 else cred_cnt
              j = 1
          jz = {}
        continue
      g = m.groups()
      if len(g) > 1:
        jz[g[0]] = jz.get(g[0], 0) + int(g[1])
        j += int(g[1])
    for jz_key in jz:
      if 24 <= jz[jz_key] and jz[jz_key] < 44:
        cred_cnt += 1
        print("===", hex(h))
        if h == 0x8026340:
          print("yeah")
          break

    x.append(h)
    y.append(j)
    xy.append((h, j))

print(cred_cnt)
xy = sorted(xy, key=itemgetter(1))
# for i in xy:
#   print(hex(i[0]), i[1])
#   if i[0] == 0xc301:
#     print("asdf", i[1], "asdf")


# print(len(x), len(y))
# fig, ax = plt.subplots()
# ax.plot(x, y)
# ax.grid()
# plt.show()