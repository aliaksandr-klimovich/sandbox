"""
Based on https://en.wikipedia.org/wiki/Piano_key_frequencies
    and ATtiny13A datasheet

Task:
    Calculate best-fit frequencies for ATtiny13A MCU
    that should match piano tones (according to wiki page)
    having (according to datasheet) only one 8-bit timer and 8, 64, 256 and 1024 prescaler.

"""
from io import StringIO
from collections import defaultdict
from pprint import pprint

import re

wiki_text = """Номер клавиши	Нота	Английская нотация	Частота (Гц).
88	до7	C8	4186,01
87	си6	B7	3951,07
86	ля♯6 (си♭6)	A♯7/B♭7	3729,31
85	ля6	A7	3520,00
84	соль♯6 (ля♭6)	G♯7/A♭7	3322,44
83	соль6	G7	3135,96
82	фа♯6 (соль♭6)	F♯7/G♭7	2959,96
81	фа6	F7	2793,83
80	ми6	E7	2637,02
79	ре♯6 (ми♭6)	D♯7/E♭7	2489,02
78	ре6	D7	2349,32
77	до♯6 (ре♭6)	C♯7/D♭7	2217,46
76	до6	C7	2093,00
75	си5	B6	1975,53
74	ля♯5 (си♭5)	A♯6/B♭6	1864,66
73	ля5	A6	1760,00
72	соль♯5 (ля♭5)	G♯6/A♭6	1661,22
71	соль5	G6	1567,98
70	фа♯5 (соль♭5)	F♯6/G♭6	1479,98
69	фа5	F6	1396,91
68	ми5	E6	1318,51
67	ре♯5 (ми♭5)	D♯6/E♭6	1244,51
66	ре5	D6	1174,66
65	до♯5 (ре♭5)	C♯6/D♭6	1108,73
64	до5	C6	1046,50
63	си4	B5	987,767
62	ля♯4 (си♭4)	A♯5/B♭5	932,328
61	ля4	A5	880,000
60	соль♯4 (ля♭4)	G♯5/A♭5	830,609
59	соль4	G5	783,991
58	фа♯4 (соль♭4)	F♯5/G♭5	739,989
57	фа4	F5	698,456
56	ми4	E5	659,255
55	ре♯4 (ми♭4)	D♯5/E♭5	622,254
54	ре4	D5	587,330
53	до♯4 (ре♭4)	C♯5/D♭5	554,365
52	до4	C5	523,251
51	си3	B4	493,883
50	ля♯3 (си♭3)	A♯4/B♭4	466,164
49	ля3	A4	440,000
48	соль♯3 (ля♭3)	G♯4/A♭4	415,305
47	соль3	G4	391,995
46	фа♯3 (соль♭3)	F♯4/G♭4	369,994
45	фа3	F4	349,228
44	ми3	E4	329,628
43	ре♯3 (ми♭3)	D♯4/E♭4	311,127
42	ре3	D4	293,665
41	до♯3 (ре♭3)	C♯4/D♭4	277,183
40	до3	C4	261,626
39	си2	B3	246,942
38	ля♯2 (си♭2)	A♯3/B♭3	233,082
37	ля2	A3	220,000
36	соль♯2 (ля♭2)	G♯3/A♭3	207,652
35	соль2	G3	195,998
34	фа♯2 (соль♭2)	F♯3/G♭3	184,997
33	фа2	F3	174,614
32	ми2	E3	164,814
31	ре♯2 (ми♭2)	D♯3/E♭3	155,563
30	ре2	D3	146,832
29	до♯2 (ре♭2)	C♯3/D♭3	138,591
28	до2	C3	130,813
27	си1	B2	123,471
26	ля♯1 (си♭1)	A♯2/B♭2	116,541
25	ля1	A2	110,000
24	соль♯1 (ля♭1)	G♯2/A♭2	103,826
23	соль1	G2	97,9989
22	фа♯1 (соль♭ 1)	F♯2/G♭2	92,4986
21	фа1	F2	87,3071
20	ми1	E2	82,4069
19	ре♯1 (ми♭1)	D♯2/E♭2	77,7817
18	ре1	D2	73,4162
17	до♯1 (ре♭1)	C♯2/D♭2	69,2957
16	до1	C2	65,4064
15	си0	B1	61,7354
14	ля♯0 (си♭0)	A♯1/B♭1	58,2705
13	ля0	A1	55,0000
12	соль♯0 (ля♭0)	G♯1/A♭1	51,9130
11	соль0	G1	48,9995
10	фа♯0 (соль♭0)	F♯1/G♭1	46,2493
9	фа0	F1	43,6536
8	ми0	E1	41,2035
7	ре♯0 (ми♭0)	D♯1/E♭1	38,8909
6	ре0	D1	36,7081
5	до♯0 (ре♭0)	C♯1/D♭1	34,6479
4	до0	C1	32,7032
3	си−1	B0	30,8677
2	ля♯−1 (си♭−1)	A♯0/B♭0	29,1353
1	ля−1	A0	27,5000
"""

# remove header
t = wiki_text.splitlines()
del t[0]
t = '\n'.join(t)

note = []
freq = []

r = re.compile('(.+?)\t(.+?)\t(.+?)\t(.+)')
for m in r.finditer(t):
    n = m[3]
    note.append(n)
    f = float(m[4].replace(',', '.'))
    freq.append(f)

CLK = 9_600_000  # actual clock frequency
CLK_PRESCALER = 8  # clock prescaler (internal prescaler set by fuse)

CLKS = {}

# all possible frequencies that can be generated using MCU
CLKS[8] = [(CLK / CLK_PRESCALER / 8 / i, i) for i in range(1, 256)]
CLKS[64] = [(CLK / CLK_PRESCALER / 64 / i, i) for i in range(1, 256)]
CLKS[256] = [(CLK / CLK_PRESCALER / 256 / i, i) for i in range(1, 256)]
CLKS[1024] = [(CLK / CLK_PRESCALER / 1024 / i, i) for i in range(1, 256)]

#pprint(CLKS)

# to find the most near frequency in l near to f
def find_near(f, l):
    li = iter(l)  # list iterator
    prev = next(li)
    prev_f, prev_div = prev
    if f > prev_f:
        return prev_f, prev_div
    for cur_f, cur_div in li:
        if prev_f >= f >= cur_f:
            if prev_f - f > f - cur_f:
                return cur_f, cur_div
            else:
                return prev_f, prev_div
        prev_f, prev_div = cur_f, cur_div
    return cur_f, cur_div

clks = defaultdict(list)

# find tones for each MCU frequency
for f in freq:
    for i in CLKS:
        f_n, div = find_near(f, CLKS[i])
        clks[i].append((f_n, div))

#pprint(list(zip(freq, clks[64])))

# find MCU frequency that better fits in tone
best_fit = []

clk2 = []  # reorganize data to be able to iterate over all clocks
for c in clks:
    clk2.append([[*i, c] for i in clks[c]])

#pprint(clk2)

for pac in zip(freq, *clk2):
   f = pac[0]
   cl = pac[1:]  # [f2, div, clk]
   m = [(abs(f - c[0]), c) for c in cl]
   best = min(m, key=lambda i: i[0])
   best_fit.append(best[1])

best_fit = list(zip(*best_fit))  # 3 lists, [0] - actual MCU freq., [1] - dividor, [2] - clk prescaler

# round calculated MCU freq., leave 2 digits after point
best_fit[0] = list(best_fit[0])
for i in range(len(best_fit[0])):
    best_fit[0][i] = round(best_fit[0][i], ndigits=2)

# visualize data :)
code = [f'{i:08b}' for i in range(len(note))][::-1]
from exercises.table_builder import TextTableBuilder
tb = TextTableBuilder(
    ['Note', 'Freq.', 'Calc.freq.', 'Div.', 'clk', 'code'],
    [note, freq, best_fit[0], best_fit[1], best_fit[2], code],
    style=TextTableBuilder.HeavyAndLightStyle
)

print()

idxG6 = note.index('C8')
idxC4 = note.index('G3')
# print(idxG6, idxC4)

# remove ♭ from notes
for i in range(len(note)):
    l = note[i].split('/')
    n = l[0]
    n = n.replace('♯', '#')
    note[i] = n

buf = StringIO()

print(';... ... ', end='', file=buf)
j = 0
for i in reversed(range(idxG6+1, idxC4+1)):
    print(f'{j:02X}, ', end='', file=buf)
    j += 1
print(f'{j:02X}', file=buf)

print(';... ... ', end='', file=buf)
for i in reversed(range(idxG6+1, idxC4+1)):
    print(note[i], end=', ', file=buf)
print(note[idxG6], file=buf)

print('tone_tb: .db ', end='', file=buf)
for i in reversed(range(idxG6+1, idxC4+1)):
    print(best_fit[1][i], end=', ', file=buf)
print(best_fit[1][idxG6], file=buf)

print('clock_tb: .db ', end='', file=buf)
for i in reversed(range(idxG6+1, idxC4+1)):
    print('clk' + str(best_fit[2][i]), end=', ', file=buf)
print('clk' + str(best_fit[2][idxG6]), file=buf)

s = buf.getvalue()
buf.close()

# print(s)
from exercises.align import align
print(align(s))

# print()
# buf = StringIO()
