"""
Very experimental =)
"""

MODE = 'DIS'  # TIMEIT, DIS

if MODE == 'TIMEIT':

    from timeit import Timer

    arr_size = 1000000
    t = 10
    for f_name, op, im in (
            ('reduce', f'list(reduce(list(range({arr_size}))))', 'from reduce import reduce'),
            ('reduce2', f'list(reduce2(list(range({arr_size}))))', 'from reduce2 import reduce2'),
            ('get_reduced_list',
             f'get_reduced_list(list(range({arr_size})))', 'from get_reduced_list import get_reduced_list'),
            ('get_reduced_list2',
             f'get_reduced_list2(list(range({arr_size})))', 'from get_reduced_list2 import get_reduced_list2'),
            ('get_reduced_list3',
             f'get_reduced_list3(list(range({arr_size})))', 'from get_reduced_list3 import get_reduced_list3'),
    ):
        print(f'{f_name}: {round(Timer(op, im).timeit(t), 3)}[s]')

elif MODE == 'DIS':

    from dis import dis, code_info
    from reduce import reduce

    print(code_info(reduce))
    # print(code_info(reduce2))
    # print(code_info(get_reduced_list))
    # print(code_info(get_reduced_list2))
    # print(code_info(get_reduced_list3))
    # print(dis(reduced))
    print(dis(reduce))
    # print(dis(get_reduced_list))
    # print(dis(get_reduced_list2))
    # print(dis(get_reduced_list3))
