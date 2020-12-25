from copy import deepcopy
from bit import Bit
from bit_field import BitField


class Register:
    """
    Representation of the HW register.

    User should define bits and bit fields as class properties.

    Several helpful structures are defined:
    self._bits       : List of `Bit`s of the register instance.
    self._bit_fields : List of `BitField`s of the register instance.
    """

    def __init__(self, value: int, mask: int = None):
        self.value = value
        self.mask = mask

        if mask is None:
            self.masked_value = value
        else:
            self.masked_value = value & mask

        # helpers
        self.bits = []
        self.bit_fields = []

        self._load()

    def __getitem__(self, index):
        """
        Get bit value by its index.

        If using slice, mind that bit counting starts from the right, e.g.
        | 1 | 0 | 1 | 0 |  value
        | 3 | 2 | 1 | 0 |  bit number
        slice reg[2:3] will give 0b10 result same as reg[3:2]

        :param index: Bit index in the register
        :return: Bit value or bit field value.
        """

        if isinstance(index, int):
            return self.masked_value >> index & 1

        elif isinstance(index, slice):
            slice_ = index
            val = 0
            step = 1 if slice_.start < slice_.stop else -1
            for i in range(slice_.start, slice_.stop + step, step):
                val |= 1 << i & self.masked_value
            # get short value
            val >>= min(slice_.start, slice_.stop)
            return val

        raise IndexError(f'Bit number {index} is not defined in {self.__class__.__name__} class')

    def _load(self):
        """Loads value passed to the class initializer and parses it into bits and bit fields."""

        # Iterate over class properties
        for attr_name in dir(self.__class__):

            # All magic is excluded
            if attr_name.startswith('_'):
                continue

            attr = getattr(self.__class__, attr_name)

            if isinstance(attr, Bit):
                bit = self._copy_instance(attr_name, attr)
                self.bits.append(bit)
                bit.value = self.masked_value >> bit.index & 1

            elif isinstance(attr, BitField):
                bit_field = self._copy_instance(attr_name, attr)
                self.bit_fields.append(bit_field)
                bit_field.value = self._get_short_value(self.masked_value, bit_field.mask)

    def _copy_instance(self, name, instance):
        instance_copy = deepcopy(instance)
        setattr(self, name, instance_copy)
        return instance_copy

    @staticmethod
    def _get_short_value(value: int, mask: int) -> int:
        """
        Composes new value from given value selecting only bits present in mask (ones).

        Example:
        |1|1|0|0| <- value
        |0|1|0|1| <- mask
        | |1| |0| <- masked value and the result, i.e. 0b_10

        :param value: Register value.
        :param mask: Register mask.
        :return: Short value: Such bits are extracted from value where mask at the same position contains 1.
        """
        res = 0
        i = 0
        while mask and value:
            if mask & 1:
                if value & 1:
                    res |= 1 << i
                i += 1
            mask >>= 1
            value >>= 1
        return res

    def __eq__(self, other) -> bool:
        assert isinstance(other, self.__class__)
        return self.masked_value == other.masked_value
