import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

FONT_SIZE = 'MAX'
FONT_PATH = '/Library/Fonts/Georgia Italic.ttf'
DISPLAY_WIDTH, DISPLAY_HEIGHT = 128, 64


def char_to_pixels(text, path, font_size):
    font = ImageFont.truetype(path, font_size)
    w, h = font.getsize(text)
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)  # inverse
    return arr


def generate_char(char, width, height, font_size=FONT_SIZE):
    arr = char_to_pixels(char, path=FONT_PATH, font_size=font_size)

    # cut top
    for top, row in enumerate(arr):
        if any(row):
            break
    arr = arr[top:]

    # cut bottom
    for bottom, row in enumerate(arr[::-1]):
        if any(row):
            break
    bottom = arr.shape[0] - bottom
    arr = arr[:bottom]

    # cut left
    for left, col in enumerate(arr.T):
        if any(col):
            break
    arr = arr.T[left:].T

    # cut right
    for right, col in enumerate(arr.T[::-1]):
        if any(col):
            break
    right = arr.shape[1] - right
    arr = arr.T[:right].T

    h, w = arr.shape
    # max_width = w if w > max_width else max_width
    # max_height = h if h > max_height else max_height

    if w > width:
        raise Exception()
        # print(f'Cannot fit in width={width}. Width of character \'{char}\' is {w}.')

    if h > height:
        raise Exception()
        # print(f'Cannot fit in height={height}. Height of character \'{char}\' is {h}.')

    def insert_left(arr, num):
        l = arr.tolist()
        for i in range(num):
            for row in l:
                row.insert(0, 0)
        a = np.array(l)
        return a

    def insert_right(arr, num):
        l = arr.tolist()
        for i in range(num):
            for row in l:
                row.append(0)
        a = np.array(l)
        return a

    def insert_top(arr, num):
        l = arr.tolist()
        new_row = [0] * len(l[0])
        for i in range(num):
            l.insert(0, new_row)
        a = np.array(l)
        return a

    def insert_bottom(arr, num):
        l = arr.tolist()
        new_row = [0] * len(l[0])
        for i in range(num):
            l.append(new_row)
        a = np.array(l)
        return a

    awidth, aheight = (width - w) // 2, (height - h) // 2
    arr = insert_left(arr, awidth)
    arr = insert_right(arr, awidth)
    arr = insert_top(arr, aheight)
    arr = insert_bottom(arr, aheight)
    if awidth * 2 + w == width - 1:
        arr = insert_right(arr, 1)
    if aheight * 2 + h == height - 1:
        arr = insert_top(arr, 1)

    return arr


def get_clock_characters(numbers_width=(DISPLAY_WIDTH // 5), font_size=FONT_SIZE):
    numbers = []
    for char in '0123456789':
        number = generate_char(char, numbers_width, DISPLAY_HEIGHT, font_size)
        numbers.append(number)

    w = DISPLAY_WIDTH - numbers_width * 4
    colon = generate_char(':', w, DISPLAY_HEIGHT, font_size)

    return numbers, colon


def find_max_size_for_clock_characters(MIN_NUM_WIDTH=25, MAX_NUM_WIDTH=40, MIN_FONT_SIZE=40, MAX_FONT_SIZE=80):
    max_num_width = 0
    max_num_width_pair = None
    max_f_size = 0
    max_f_size_pair = None

    for num_width in range(MIN_NUM_WIDTH, MAX_NUM_WIDTH):
        for f_size in range(MIN_FONT_SIZE, MAX_FONT_SIZE):
            try:
                get_clock_characters(num_width, f_size)
            except Exception:
                pass
            else:
                if num_width > max_num_width:
                    max_num_width = num_width
                    max_num_width_pair = (num_width, f_size)
                if f_size > max_f_size:
                    max_f_size = f_size
                    max_f_size_pair = (num_width, f_size)

    print(f'max_num_width = {max_num_width}')
    print(f'max_num_width_pair = {max_num_width_pair}\n')
    print(f'max_f_size = {max_f_size}')
    print(f'max_f_size_pair = {max_f_size_pair}\n')

    return max_f_size_pair


def get_c_array_init_line_from_np_array(arr):
    # uint8_t
    l = arr.tolist()

    new_l = []
    for y in range(len(l[0])):
        for x in range(len(l)):
            new_l.append(l[x][y])
    l = [new_l[i:i + 8] for i in range(0, len(new_l), 8)]

    buf = []
    buf.append('  {')
    for uint8 in l:
        uint8 = (str(i) for i in uint8)
        uint8 = "".join(uint8)
        uint8 = "".join([v for v in reversed(uint8)])
        uint8 = int(uint8, 2)
        buf.append(f'0x{uint8:02X}')
        buf.append(',')
    buf.pop()
    buf.append('},')
    s = "".join(buf)
    return s


def main():
    if FONT_SIZE == 'MAX':
        numbers_width, font_size = find_max_size_for_clock_characters()
    else:
        numbers_width, font_size = 30, FONT_SIZE
    numbers, colon = get_clock_characters(numbers_width, font_size)

    # print them!
    for arr in numbers + [colon]:
        height, width = arr.shape
        print(f'(height={height}, width={width})')
        for row in arr.tolist():
            print(row)
        print()

    # generate defines
    width = numbers[0].shape[1]
    print(f'#define NUMBER_WIDTH ({width * 8})')
    width = colon.shape[1]
    print(f'#define COLON_WIDTH ({width * 8})')

    # generate C code
    print('uint8_t bigClockFont[][' + str(numbers_width * DISPLAY_HEIGHT // 8) + '] = {')
    for arr in numbers + [colon]:
        print(get_c_array_init_line_from_np_array(arr))
    print('};')


if __name__ == '__main__':
    main()
