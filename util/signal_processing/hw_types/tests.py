import unittest
from bit import Bit
from bit_field import BitField
from register import Register


class RegisterUsageExample(unittest.TestCase):

    def test(self):

        # This is example is based on the Attiny85 reference manual.
        # One of the registers of Attiny85 is described.

        class WDTCR(Register):
            """Watchdog Timer Control Register"""

            # bits definition
            WDP0 = Bit(0, value=0)  # value is optional, but here present for demonstrative purposes
            WDP1 = Bit(1, 0)
            WDP2 = Bit(2, 0)
            WDE  = Bit(3, value='X')  # init value is undefined, 'X' is a user parameter and not processed
            WDCE = Bit(4, 0)
            WDP3 = Bit(5, 0)
            WDIE = Bit(6, 0)
            WDIF = Bit(7, 0)

            # bit field can unite several bits
            WDP = BitField(WDP3, WDP2, WDP1, WDP0, value=0)  # value is optional

            # custom properties
            _ADR = 0x21
            _BIT_COUNT = 8
            _MASK = 0b_1111_0111

            # more custom properties (these are accessible through class instance)
            @property
            def watchdog_time_state(self):
                return {
                    0b00: 'Stopped',
                    0b01: 'Running',
                    0b10: 'Running',
                    0b11: 'Running',
                }[self.WDE.value << 1 | self.WDIE.value]

            @property
            def action_on_timeout(self):
                return {
                    0b00: 'None',
                    0b01: 'Interrupt',
                    0b10: 'Reset',
                    0b11: 'Interrupt',
                }[self.WDE.value << 1 | self.WDIE.value]
            
            @property
            def number_of_wdt_oscillator_cycles(self):
                return {i: 2048 * 2 ** i for i in range(10)}[self.WDP.value]

            @number_of_wdt_oscillator_cycles.setter
            def number_of_wdt_oscillator_cycles(self, n):
                self.WDP.value = {2048 * 2 ** i: i for i in range(10)}[n]

        # Class attributes are accessible before class instance creation.
        # bit index and value
        self.assertEqual(WDTCR.WDP0.index, 0)
        self.assertEqual(WDTCR.WDP0.value, 0)
        self.assertEqual(WDTCR.WDE.value, 'X')
        # bit field mask
        self.assertEqual(WDTCR.WDP.mask, 0b_0010_0111)  # mask is built based on the defined bits in bit field
        # bit field value
        self.assertEqual(WDTCR.WDP.value, 0)

        # Instance should contain a value stored in the register.
        # All bits and fields will be copied to the instance.
        wdtcr = WDTCR(0b_1110_0111)
        # Still can access bits, but mind new object!
        # Class property `value` differs from instance property `value`.
        # First is defined in the class, second comes from the instance initialization argument.
        self.assertEqual(WDTCR.WDIF.value, 0)  # set in class as a property
        self.assertEqual(wdtcr.WDIF.value, 1)  # set by user at instance creation

        # It is possible to have a direct indexing of the bit.
        # In this case value is returned.
        self.assertEqual(wdtcr[5], 1)
        # Also can use slices. Both borders are set inclusively. Order of bit doesn't matter.
        # The return value is calculated based on the descending order of bits:
        #  e.g. 3 - 2 - 1 - 0
        #       |   |
        #       0   1  <- returned value
        self.assertEqual(wdtcr[2:3], 0b01)
        self.assertEqual(wdtcr[3:2], 0b01)

        # Custom properties can be used.
        self.assertEqual(wdtcr.watchdog_time_state, 'Running')
        self.assertEqual(wdtcr.action_on_timeout, 'Interrupt')

        # Demonstrate property setter
        self.assertEqual(wdtcr.WDP.value, 0b_1111)
        # Currently this value is reserved so number_of_wdt_oscillator_cycles getter should raise a KeyError:
        with self.assertRaises(KeyError):
            _ = wdtcr.number_of_wdt_oscillator_cycles
        # Can fix WDP setting it to correct value
        wdtcr.number_of_wdt_oscillator_cycles = 4096
        # And now the WDP value is also different
        self.assertEqual(wdtcr.WDP.value, 1)

        # todo Bits and bit fields can be compared.
        pass

        # todo Registers can be compared.
        pass


if __name__ == '__main__':
    unittest.main()
