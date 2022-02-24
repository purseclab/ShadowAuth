import glob, os
import numpy as np
from operator import itemgetter, attrgetter

def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)


x = []
y = []

xy = []


path = 'rusefi'
all = len(os.listdir(os.path.join(os.getcwd(), path)))
cur = 1
for filename in os.listdir(os.path.join(os.getcwd(), path)):
  print(f"{cur}/{all}")
  cur += 1
  j = 1
  max_j = 0
  with open(os.path.join(os.getcwd(), path, filename), 'r') as f: # open in readonly mode
    h = row2_to_int(filename.split(".")[0])
    for line in f:
      if line.lower().startswith("*[ram]unique["):
        j = j + 1
        max_j = j if j > max_j else max_j
        # print(line)
      else:
        j = j - 1  if j > 1 else 1
    x.append(h)
    y.append(max_j)
    xy.append((h, max_j))

xy = sorted(xy, key=itemgetter(1))
for i in xy:
  print(hex(i[0]), i[1])

# print(len(x), len(y))
# fig, ax = plt.subplots()
# ax.plot(x, y)
# ax.grid()
# plt.show()