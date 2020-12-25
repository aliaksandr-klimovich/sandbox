from functools import reduce
from bit import Bit


class BitField:
    """
    Represents bit field (2+ linked bits) in a register.
    The most important attribute here is the `mask`. It defines a bit field.
    """
    def __init__(self, *args, **kwargs):
        """
        Supports next variants of initialization:
        1) BitField(0b_0001) - where first argument is a full register mask
        2) BitField(mask=0b_0010) - same, but with a keyword
        3) BitField(Bit(2), Bit(1), Bit(0)) - mask is calculated based on the passed in bits, order is not important
        4) todo BitField(BitField(0b_0011), BitField(0b_1100)) - can build a mask based on other bit fields
        Any extra user keyword is stored in the instance.
        """
        # todo fix situation when mask is given as a kwg and bit is given as arg, i.e. multiple conditions
        if args and isinstance(args[0], int):
            self.mask = args[0]
        elif all((isinstance(bit, Bit) for bit in args)):
            # Get mask from `Bit`s, do not store `Bit` instances.
            self.mask = reduce(lambda m, bit: m | 1 << bit.index, args, 0)
        elif 'mask' in kwargs:
            self.mask = kwargs['mask']
        else:
            raise ValueError('Invalid mask')

        if 'value' in kwargs:
            self.value = kwargs['value']
        else:
            self.value = None

    def __eq__(self, other) -> bool:
        assert isinstance(other, self.__class__)
        return self.mask == other.mask and self.value == other.value
