import math

in_num = 'f100'
in_base = 16
out_base = 2

digit_additions = ['a', 'b', 'c', 'd', 'e', 'f']

def convert_to_num(digit):
    try:
        return int(digit)
    except ValueError:
        if digit == '.':
            return '.'
        return digit_additions.index(digit) + 10

in_digits = []
for digit_index in range(1, len(in_num) + 1):
    in_digits.append(convert_to_num(in_num[len(in_num) - digit_index]))

decimal_index = -1
if '.' in in_digits:
    decimal_index = in_digits.index('.')

if not decimal_index == -1:
    frac = in_digits[0:decimal_index]
    print('decimal digit is', decimal_index)
    print(decimal_index + 1)
    print(len(in_digits))
    whole_number = in_digits[(decimal_index + 1): len(in_digits)]
else:
    whole_number = in_digits.copy()
    frac = []

whole_number_sum = 0
for i in range(0, len(whole_number)):
    whole_number_sum += in_base**i * whole_number[i]

whole_number_answer = ''
while whole_number_sum > 0:
    whole_number_answer = str(whole_number_sum % out_base) + whole_number_answer
    whole_number_sum = int(whole_number_sum / out_base)

frac.reverse()
frac_sum = 0
for i in range(1, len(frac) + 1):
    frac_sum += in_base**-i * frac[i-1]
print('frac is', frac)

frac_answer = ''
while math.fabs(frac_sum - 0) > 0.000000001:
    print('frac sum is', frac_sum)
    frac_sum *= float(out_base)
    if frac_sum > 1:
        frac_answer = frac_answer + str(int(frac_sum))
        frac_sum -= int(frac_sum)
    else:
        frac_answer = frac_answer + '0'


print(whole_number_answer + '.' + frac_answer)
