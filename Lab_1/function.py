import math as m

class Function:

    @staticmethod
    def call_function(n0, h, nk, a, b, c):
        result_dict = {}
        x = n0
        while x <= nk:
            result = a * m.sin(x) + b * m.cos(x) + abs(a * m.sin(x) - b * m.cos(x)) + c
            result_dict[x] = result
            x += h

        return result_dict
