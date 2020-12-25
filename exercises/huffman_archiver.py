from functools import reduce
from operator import itemgetter

# Get text.
text = 'simple test'
print(f'text: {text}')

# Count each char in text.
pairs = []
for char in text:
    for pair in pairs:
        if pair[0] == char:
            pair[1] += 1
            break
    else:
        pairs.append([char, 1])
print(f'pairs: {pairs}')

# Build tree.
while True:
    try:
        min1 = min(pairs, key=itemgetter(1))
        pairs.remove(min1)
    except ValueError:
        break

    try:
        min2 = min(pairs, key=itemgetter(1))
        pairs.remove(min2)
    except ValueError:
        pairs.append(min1)
        break

    pairs.append([min1[0] + min2[0], min1[1] + min2[1], [min1, min2]])
print(f'tree: {pairs}')

# Tree traversal. Build encoding table.
table = []
def f(l, code=''):
    if len(l) == 2:
        table.append((l[0], code))
    else:
        code0 = code + '0'
        code1 = code + '1'
        f(l[2][0], code0)
        f(l[2][1], code1)

f(pairs[0])
print(f'table: {table}')

# Encode text.
table_dict = dict(table)
encoded = ''.join((table_dict[i] for i in text))
print(f'text_encoded: {encoded}')

# Decode text.
decoded = []
index = 0
code = ''
while index < len(encoded):
    code += encoded[index]
    index += 1
    for char, c in table:
        if c == code:
            decoded.append(char)
            code = ''
            break
decoded = ''.join(decoded)
print(f'text_decoded: {decoded}')

# Statistics.
print('\nText length: %i bits' % (len(text) * 8))
print('Encoded text length: %i bits' % len(encoded))
print('Table size: %i ?' % reduce(lambda s, i: 1 + len(i[1]) + s, table, 0))
# todo check table size
