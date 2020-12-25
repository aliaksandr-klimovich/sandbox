class Bit:
    """
    Represents a bit in a register.
    """
    def __init__(self, index, value=None):
        """
        :param index: Index of the bit.
        :param value: Initial value of the bit.
        """
        self.index = index
        self.value = value

    def __eq__(self, other) -> bool:
        assert isinstance(other, self.__class__)
        return self.index == other.index and self.value == other.value
