from string import ascii_letters

c_file_name = 'avr_map.c'
h_file_name = 'avr_map.h'
LAST_PAD_LETTER = 'D'
NUMBER_OF_PINS_IN_PAD = 8

pads = ascii_letters[ascii_letters.index('A'):ascii_letters.index(LAST_PAD_LETTER)+1]
pins = range(NUMBER_OF_PINS_IN_PAD)

c_file_text = ''

c_includes = '#include <avr/io.h>\n#include "avr_map.h"'
c_file_text += c_includes

c_pins = []
for pad in pads:
    for pin in pins:
        c_pins.append(f'PIN P{pad}{pin} = {{&DDR{pad}, &PORT{pad}, &PIN{pad}, {pin}}};')
    c_pins.append('')
c_pins = '\n'.join(c_pins)
c_file_text += f'\n\n{c_pins}'

h_file_text = ''

h_head = """/*

  AVR pin mapping

  This module re-defines standard port mapping (aka PB1, PD3...) to PIN (struct) mapping.
  See avr_map.c for more details.

*/"""

def add_h_defines(text, name):
    return f'#ifndef {name}\n#define {name}\n\n{text}\n\n#endif /* {name} */'

h_includes = '#include "pin_type.h"'
h_file_text += h_includes

h_pins = []
for pad in pads:
    for pin in pins:
        h_pins.append(f'#ifdef P{pad}{pin}\n#undef P{pad}{pin}\n#endif\nextern PIN P{pad}{pin};')
        h_pins.append('')
h_pins = '\n'.join(h_pins)
h_file_text += f'\n\n{h_pins}'

h_file_text = add_h_defines(h_file_text, 'AVR_MAP_H_')

h_file_text = f'{h_head}\n\n{h_file_text}'

print(h_file_text)


