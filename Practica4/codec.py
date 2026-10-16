import struct

OPCODES = {
    'push': 1, 'add': 2, 'sub': 3, 'mul': 4, 'div': 5,
    'dup': 6, 'swap': 7, 'drop': 8, 'get': 9, 'put': 10,
    'jz': 11, 'j': 12, 'halt': 13
}
OPCODE_NAMES = {v: k for k, v in OPCODES.items()}


def encode(code):
    """Кодирование списка команд стековой ВМ в байты."""
    data = b''
    for instr in code:
        op = instr[0]
        if op not in OPCODES:
            raise ValueError(f"Unknown op: {op}")
        data += struct.pack('B', OPCODES[op])
        if op in ('push', 'jz', 'j'):
            arg = instr[1]
            data += struct.pack('>i', arg)
    return data


def decode(data):
    """Декодирование байтов обратно в список команд."""
    code = []
    i = 0
    while i < len(data):
        opcode = data[i]
        i += 1
        op = OPCODE_NAMES[opcode]
        if op in ('push', 'jz', 'j'):
            arg = struct.unpack('>i', data[i:i+4])[0]
            i += 4
            code.append((op, arg))
        else:
            code.append((op,))
    return code


def save(filename, code):
    with open(filename, 'wb') as f:
        f.write(encode(code))


def load(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return decode(data)


if __name__ == '__main__':
    # Пример: сумма чисел до нуля
    program = [
        ('push', 0),
        ('get',),
        ('dup',),
        ('jz', 6),
        ('add',),
        ('j', 1),
        ('drop',),
        ('put',),
        ('halt',)
    ]
    save('sum.bin', program)
    loaded = load('sum.bin')
    print("Исходная программа:", program)
    print("Загруженная программа:", loaded)