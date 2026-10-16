class RegVM:
    def __init__(self):
        self.regs = [0] * 16
        self.pc = 0

    def run(self, code):
        self.pc = 0
        while self.pc < len(code):
            op, *args = code[self.pc]
            self.pc += 1

            if op == 'move':
                self.regs[args[0]] = args[1]
            elif op == 'add':
                self.regs[args[0]] = self.regs[args[1]] + self.regs[args[2]]
            elif op == 'sub':
                self.regs[args[0]] = self.regs[args[1]] - self.regs[args[2]]
            elif op == 'mul':
                self.regs[args[0]] = self.regs[args[1]] * self.regs[args[2]]
            elif op == 'div':
                self.regs[args[0]] = self.regs[args[1]] // self.regs[args[2]]
            elif op == 'get':
                self.regs[args[0]] = int(input("<- "))
            elif op == 'put':
                print("->", self.regs[args[0]])
            elif op == 'jz':
                if self.regs[args[0]] == 0:
                    self.pc = args[1]
            elif op == 'j':
                self.pc = args[0]
            elif op == 'halt':
                break


def discriminant(a, b, c):
    """D = b^2 - 4ac на регистровой ВМ."""
    code = [
        ('move', 0, b),          # r0 = b
        ('mul', 0, 0, 0),        # r0 = b^2
        ('move', 1, 4),          # r1 = 4
        ('move', 2, a),          # r2 = a
        ('mul', 1, 1, 2),        # r1 = 4a
        ('move', 2, c),          # r2 = c
        ('mul', 1, 1, 2),        # r1 = 4ac
        ('sub', 0, 0, 1),        # r0 = b^2 - 4ac
        ('put', 0),              # вывод r0
        ('halt',)
    ]
    vm = RegVM()
    vm.run(code)


def sum_input():
    """Сумма чисел до нуля на регистровой ВМ."""
    code = [
        ('move', 0, 0),          # r0 = 0 (sum)
        ('get', 1),              # 1: loop, r1 = input
        ('jz', 1, 6),            # 2: if r1 == 0 goto done
        ('add', 0, 0, 1),        # 3: r0 += r1
        ('j', 1),                # 4: goto loop
        ('put', 0),              # 5: done, вывод r0
        ('halt',)                # 6
    ]
    vm = RegVM()
    vm.run(code)


if __name__ == '__main__':
    print("Дискриминант для a=1, b=5, c=6:")
    discriminant(1, 5, 6)

    print("\nСумма чисел (0 для выхода):")
    sum_input()