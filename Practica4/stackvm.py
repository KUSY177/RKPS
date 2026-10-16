class StackVM:
    def __init__(self):
        self.stack = []
        self.pc = 0
        self.code = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        return self.stack.pop()

    def run(self, code):
        self.code = code
        self.pc = 0
        while self.pc < len(self.code):
            op, *args = self.code[self.pc]
            self.pc += 1

            if op == 'push':
                self.push(args[0])
            elif op == 'add':
                b = self.pop(); a = self.pop(); self.push(a + b)
            elif op == 'sub':
                b = self.pop(); a = self.pop(); self.push(a - b)
            elif op == 'mul':
                b = self.pop(); a = self.pop(); self.push(a * b)
            elif op == 'div':
                b = self.pop(); a = self.pop(); self.push(a // b)
            elif op == 'dup':
                self.push(self.stack[-1])
            elif op == 'swap':
                a = self.pop(); b = self.pop(); self.push(a); self.push(b)
            elif op == 'drop':
                self.pop()
            elif op == 'get':
                self.push(int(input("<- ")))
            elif op == 'put':
                print("->", self.pop())
            elif op == 'jz':
                addr = args[0]
                if self.pop() == 0:
                    self.pc = addr
            elif op == 'j':
                self.pc = args[0]
            elif op == 'halt':
                break


def discriminant(a, b, c):
    """Вычисление дискриминанта D = b^2 - 4ac на стековой ВМ."""
    code = [
        ('push', b), ('push', b), ('mul',),          # b^2
        ('push', 4), ('push', a), ('mul',), ('push', c), ('mul',),  # 4ac
        ('sub',),                                     # b^2 - 4ac
        ('put',), ('halt',)
    ]
    vm = StackVM()
    vm.run(code)


def sum_input():
    """Сумма вводимых чисел до нуля (пример из задачи 1)."""
    code = [
        ('push', 0),          # 0: sum = 0
        ('get',),             # 1: loop
        ('dup',),             # 2
        ('jz', 6),            # 3: done
        ('add',),             # 4
        ('j', 1),             # 5: loop
        ('drop',),            # 6: done
        ('put',),             # 7
        ('halt',)             # 8
    ]
    vm = StackVM()
    vm.run(code)


if __name__ == '__main__':
    print("Дискриминант для a=1, b=5, c=6:")
    discriminant(1, 5, 6)

    print("\nСумма чисел (0 для выхода):")
    sum_input()