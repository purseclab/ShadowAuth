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
  #               name,     base,   offset,size):
  "ER_RO": Section("ER_RO", 0x8000000, 52, 0x6f8c),
}

def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)

ff = ""
def lifting(name, base, offset, size):
  LONG = False

  binary = "./elfs/sty.elf"

  if LONG is True:
    ff = open(f"str_pcode_long.txt", "w")

  langs = {l.id:l for arch in Arch.enumerate() for l in arch.languages}
  for langid in sorted(langs):
    # print('%-35s - %s' % (langid, langs[langid].description))
    pass

  langid = "ARM:LE:32:Cortex"

  with open(binary, 'rb') as f:
    f.seek(offset)
    code = f.read()


  print('%-35s - %s' % (langid, langs[langid].description))

  ctx = Context(langs[langid])
  res = ctx.translate(code, base, size, bb_terminating=False)

  if LONG is False:
    ff = open(f"sty_pcode/{name}.txt", "w")
  i = 0
  for insn in res.instructions:
    i += 1
    print (f'{i}/{len(res.instructions)}')
    if LONG:
      ff.write('-' * 80)
      ff.write("\n")
      ff.write('%08x/%d: %s %s' % (insn.address.offset, insn.length, insn.asm_mnem, insn.asm_body))
      ff.write("\n")
      ff.write('-' * 80)
      ff.write("\n")
      for op in insn.ops:
        # print('%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op)))
        a = '%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op))
        # print(a)
        ff.write(a)
        ff.write("\n")
    else: #SHORT
      for op in insn.ops:
        # ff.write('%08x ' % (insn.address.offset,))
        ff.write(PcodePrettyPrinter.fmt_op(op))
        ff.write("\n")
    # print('')
    ff.write("\n")
    # input()
  ff.close()

  if res.error:
    print('** An error occured during translation: ' + repr(res.error))


def main():
  with open("elfs/sty.elf.map", "r") as f:
    for line in f:
      row = line.split(" ")
      section = sections.get(row[1], None)
      print(row2_to_int(row[3]))
      offset = section.offset + (row2_to_int(row[2]) - section.base)
      lifting(row[2], row2_to_int(row[2]), offset, row2_to_int(row[3]))


if __name__ == "__main__":
  main()