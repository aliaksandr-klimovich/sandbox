"""
Find correct order of equations when x gets max result:

    y = z + 2
    x = y + z * 2
    x = y - 3
    z = x + y

supposing that x=1, y=2, z=3. Finally print x value.
"""

from itertools import permutations
from operator import itemgetter


functions = (
    'y = z + 2',
    'x = y + z * 2',
    'x = y - 3',
    'z = x + y',
)

# namespace where each function will be executed
ns = {}


# to reset namespace (set variables to their default values) after all functions are executed
def reset_xyz():
    ns['x'] = 1
    ns['y'] = 2
    ns['z'] = 3


# results are collected here
results = []

# pretty print =)
max_f_len = max((len(f) for f in functions)) + 1
f_row_len = len(functions) * (max_f_len + 2) - 2
msg = f' # | {"Functions to execute":{f_row_len-3}} | x'
print(msg)
print('-' * (len(msg)+2))

# iterate over all possible variants of function execution
# each function is executed only once, all functions should be executed
# only the execution order matters
for i, f_ordered in enumerate(permutations(functions), start=1):
    # set x, y, z to default values
    reset_xyz()

    # execute each function
    for f in f_ordered:
        exec(f, ns)  # execute in the given namespace

    # store result
    x = ns['x']
    results.append((i, f_ordered, x))

    # pretty print =)
    f_with_commas = (f'{f},' for f in f_ordered)
    f_with_spaces = ' '.join((f'{f:<{max_f_len}}' for f in f_with_commas))
    print(f'{i:>2} | {f_with_spaces} | {x}')

max_value = max(results, key=itemgetter(2))
print(f'\nMax. value of x: {max_value[2]}'
      f'\nCorresponding function call (row {max_value[0]}): {", ".join(max_value[1])}')
