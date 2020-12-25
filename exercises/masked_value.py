import numpy as np
import numpy.ma as ma

# Task:
#  Having array of data and mask,
#  need to obtain indexes of array values
#  after mask is applied where (7 <= value <= 8).
# Constraint:
#  If it is possible, mask should be applied only once.
#  Rationale: Filter masked data several times.

print('\n1. Solution that uses numpy.')
print('='*80)
data = [5, 4, 7, 8, 3, 2, 5, 6, 7, 8, 9, 8]
mask = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
cut_point = mask.index(1)
ma_data = ma.masked_array(data)
# also you can create and array using mask data as
# ``data = ma.masked_array(data, [not bool(i) for i in mask])``
print('            data:', ma_data)
print('            mask:', np.array(mask))
print('             idx:', np.arange(len(ma_data)))
ma_data[:cut_point] = ma.masked  # mask values till cut_point
print('     masked data:', ma_data)
# now can call ``where``
# mask is already applied and several operations can be applied without need to reapply the mask
result = ma.where((7 <= ma_data) & (ma_data <= 8))[0]  # find indexes of interest
print('filtered indexes:', result)

# Output:
# 1. Solution that uses numpy.
# ================================================================================
#             data: [5 4 7 8 3 2 5 6 7 8 9 8]
#             mask: [0 0 0 0 1 1 1 1 1 1 1 1]
#              idx: [ 0  1  2  3  4  5  6  7  8  9 10 11]
#      masked data: [-- -- -- -- 3 2 5 6 7 8 9 8]
# filtered indexes: [ 8  9 11]


print('\n2. Solution that does not use numpy.'
      '\n   Need to apply mask every data filtering (violation of task constraint).')
print('='*80)
data = [5, 4, 7, 8, 3, 2, 5, 6, 7, 8, 9, 8]
mask = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
indexes = [i for i, (d, m) in enumerate(zip(data, mask)) if m == 1 and 7 <= d <= 8]
print('indexes', indexes)

# Output:
# 2. Solution that does not use numpy.
#    Need to apply mask every data filtering (violation of task constraint).
# ================================================================================
# indexes [8, 9, 11]


print('\n3. Solution that does not use numpy.'
      '\n   Making resolved with custom class.')
print('='*80)


# solving mask issue
# make Masked class that will always return False for all compare operators
class Masked:
    def __eq__(self, other): return False
    __lt__ = __le__ = __gt__ = __ge__ = __ne__ = __eq__
    def __str__(self): return '-'
    __repr__ = __str__


# create an instance that will be used as a masked value
masked = Masked()
# mask data, replacing it with masked value
masked_data = [d if m == 1 else masked for d, m in zip(data, mask)]
print('masked data:', masked_data)
# from this point the goal is reached, now can filter data
filtered_data = [d if 7 <= d <= 8 else masked for d in masked_data]
print('filtered_data:', filtered_data)
# and get indexes
indexes = [i for i, d in enumerate(filtered_data) if d is not masked]
print('indexes:', indexes)
# filter data once again
filtered_data_2 = [d if d == 2 else masked for d in masked_data]
print('filtered_data_2:', filtered_data_2)
# and get indexes
indexes_2 = [i for i, d in enumerate(filtered_data_2) if d is not masked]
print('indexes_2:', indexes_2)

# Output:
# 3. Solution that does not use numpy.
#    Making resolved with custom class.
# ================================================================================
# masked data: [-, -, -, -, 3, 2, 5, 6, 7, 8, 9, 8]
# filtered_data: [-, -, -, -, -, -, -, -, 7, 8, -, 8]
# indexes: [8, 9, 11]
# filtered_data_2: [-, -, -, -, -, 2, -, -, -, -, -, -]
# indexes_2: [5]


# print('\n4. Solution using generator.')
# print('='*80)
# masked_data = (d for d, m in zip(data, mask) if m == 1)
# ...
# same as 3 but () instead of [] :)
