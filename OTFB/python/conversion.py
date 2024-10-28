def float_to_binary(x, m, n):
    x_scaled = round(x * 2 ** n)
    return '{:0{}b}'.format(x_scaled, m + n)

def binary_to_float(bstr, m, n):
    return int(bstr, 2) / 2 ** n

def twos_binary_to_float(bstr):
    blen = len(bstr)
    if bstr[0] == '1':
        si = int(bstr,2) - (1<<blen)
    else:
        si = int(bstr,2)
    return si

def float_to_twos_binary(fl):
    return 0
