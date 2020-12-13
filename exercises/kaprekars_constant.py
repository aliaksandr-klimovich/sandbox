# https://en.wikipedia.org/wiki/6174_(number)


def get_kaprekars_constant_equations(number, n=0):
    """
    :param n: Max. iteration before leaving.
    """
    
    def number_to_list(n):
        """returns reverted list of digits in a number"""
        res = []
        while n:
            res.append(n % 10)
            n //= 10
        return res
    
    def list_to_number(l):
        """returns reverted list of digits composed into a number"""
        res = 0
        for i, n in enumerate(l):
            res += n * 10 ** i
        return res

    while n > 0:
        # prepare to get new number
        digits = number_to_list(number)
        digits_sorted_desc = sorted(digits, reverse=True)
        digits_sorted_asc = sorted(digits, reverse=False)
        number_sorted_desc = list_to_number(digits_sorted_asc)
        number_sorted_asc = list_to_number(digits_sorted_desc)

        # get new number
        new_number = number_sorted_desc - number_sorted_asc

        yield f'{number_sorted_desc} - {number_sorted_asc} = {new_number}'

        if new_number == 6174:
            break

        # save for next iteration
        number = new_number
        n -= 1


for eq in get_kaprekars_constant_equations(4100, 10):
    print(eq)
