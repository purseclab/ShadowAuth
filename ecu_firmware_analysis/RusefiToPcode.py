from pypcode import Arch, Context, PcodePrettyPrinter

class Section:
  name = None
  base = None
  offset = None
  size = None
  def __init__(self, name, base, offset, size):
    self.name = name
    self.base = base
    self.offset = offset
    self.size = size

sections = {
  ".text": Section(".text", 0x80001f0, 66032, 280644),
}

def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)


def lifting(name, base, offset, size):
  LONG = False

  binary = "./elfs/rusefi.elf"

  langs = {l.id:l for arch in Arch.enumerate() for l in arch.languages}
  for langid in sorted(langs):
    print('%-35s - %s' % (langid, langs[langid].description))
    pass

  langid="ARM:LE:32:Cortex"

  with open(binary, 'rb') as f:
    f.seek(offset)
    code = f.read()

  print('%-35s - %s' % (langid, langs[langid].description))

  ctx = Context(langs[langid])
  res = ctx.translate(code, base, size, bb_terminating=False)

  f = open(f"rusefi/{name}.txt", "w")
  i = 0
  for insn in res.instructions:
    i += 1
    print (f'{i}/{len(res.instructions)}')
    if LONG:
      f.write('-' * 80)
      f.write("\n")
      f.write('%08x/%d: %s %s' % (insn.address.offset, insn.length, insn.asm_mnem, insn.asm_body))
      f.write("\n")
      f.write('-' * 80)
      f.write("\n")
      for op in insn.ops:
        # print('%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op)))
        a = '%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op))
        # print(a)
        f.write(a)
        f.write("\n")
    else: #SHORT
      if len(insn.ops) > 0:
        f.write(PcodePrettyPrinter.fmt_op(insn.ops[-1]))
    # print('')
    f.write("\n")
    # input()
  f.close()

  if res.error:
    print('** An error occured during translation: ' + repr(res.error))


def main():
  with open("elfs/rusefi.elf.map", "r") as f:
    for line in f:
      row = line.split(" ")
      section = sections.get(row[0], None)
      print(row2_to_int(row[2]))
      offset = section.offset + (row2_to_int(row[1]) - section.base)
      lifting(row[1], row2_to_int(row[1]), offset, row2_to_int(row[2]))


if __name__ == "__main__":
  main()