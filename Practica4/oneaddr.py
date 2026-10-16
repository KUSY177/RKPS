import sys

OPCODES = {
    'const': 0, 'get': 1, 'put': 2, 'ld': 3, 'st': 4, 'add': 5,
    'sub': 6, 'jpos': 7, 'jz': 8, 'j': 9, 'halt': 10
}
OPCODE_NAMES = {v: k for k, v in OPCODES.items()}


def assemble(source):
    """Ассемблер: первый и второй проходы + кодирование."""
    lines = []
    for line in source.splitlines():
        line = line.split('#')[0].strip()
        if not line:
            continue
        lines.append(line)

    symbol_table = {}
    intermediate = []
    address = 0

    for line in lines:
        parts = line.split()
        if parts[0] not in OPCODES and parts[0] != 'const':
            label = parts[0]
            symbol_table[label] = address
            parts = parts[1:]
        if not parts:
            continue
        op = parts[0]
        if op == 'const':
            arg = int(parts[1]) if len(parts) > 1 else 0
            intermediate.append(('const', arg))
        elif op in OPCODES:
            if len(parts) > 1:
                arg = parts[1]
                if arg.lstrip('-').isdigit():
                    arg = int(arg)
                intermediate.append((op, arg))
            else:
                intermediate.append((op, 0))
        else:
            raise ValueError(f"Unknown opcode: {op}")
        address += 1

    resolved = []
    for op, arg in intermediate:
        if isinstance(arg, str) and arg in symbol_table:
            arg = symbol_table[arg]
        resolved.append((op, arg))

    code = []
    for op, arg in resolved:
        opcode = OPCODES[op]
        code.append(opcode * 1000 + arg)

    return symbol_table, intermediate, resolved, code


class VM:
    def __init__(self, code, memory_size=100):
        self.code = code
        self.memory = [0] * memory_size
        self.acc = 0
        self.pc = 0

    def run(self):
        while True:
            instr = self.code[self.pc]
            op = instr // 1000
            arg = instr % 1000
            self.pc += 1

            if op == 0:      # const
                self.memory[self.pc - 1] = arg
            elif op == 1:    # get
                self.acc = int(input("<- "))
            elif op == 2:    # put
                print("->", self.acc)
            elif op == 3:    # ld
                self.acc = self.memory[arg]
            elif op == 4:    # st
                self.memory[arg] = self.acc
            elif op == 5:    # add
                self.acc += self.memory[arg]
            elif op == 6:    # sub
                self.acc -= self.memory[arg]
            elif op == 7:    # jpos
                if self.acc > 0:
                    self.pc = arg
            elif op == 8:    # jz
                if self.acc == 0:
                    self.pc = arg
            elif op == 9:    # j
                self.pc = arg
            elif op == 10:   # halt
                break
            else:
                raise ValueError(f"Unknown opcode: {op}")


if __name__ == '__main__':
    source = """
    # print sum of input numbers (terminated by zero)
        ld   zero    # initialize sum to zero
        st   sum
    loop get          # read a number
        jz   done    # no more input if number is zero
        add  sum     # add in accumulated sum
        st   sum     # store new value back in sum
        j    loop    # go back and read another number
    done ld   sum    # print sum
        put
        halt
    zero const 0
    sum  const
    """
    sym, inter, resolved, code = assemble(source)
    print("Symbol table:")
    print(sym)
    print("\nIntermediate code:")
    for item in inter:
        print(item)
    print("\nResolved code:")
    for i, item in enumerate(resolved):
        print(f"{i}: {item}")
    print("\nMachine code:")
    print(code)
    print("\nRunning VM (enter numbers, 0 to stop):")
    VM(code).run()