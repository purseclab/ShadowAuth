import matplotlib.pyplot as plt
import glob, os


def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)

path = './ms3_pcode'
for filename in glob.glob(os.path.join(path, '*.txt')):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
      h = row2_to_int(filename.split(".")[0])

i = 0
j = 1
x = []
y = []
with open("ms3_raw.txt", "r") as f:
  for line in f:
    x.append(i)
    if line.lower().startswith("*[ram]unique["):
      y.append(j)
      j = j * 2
      print(line)
    else:
      j = j / 2  if j > 1 else 1
      y.append(0)
    i += 1

fig, ax = plt.subplots()
ax.plot(x, y)
ax.grid()
plt.show()