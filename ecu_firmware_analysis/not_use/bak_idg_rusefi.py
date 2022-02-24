import matplotlib.pyplot as plt

i = 0
j = 1
x = []
y = []
with open("rusefi_raw.txt", "r") as f:
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