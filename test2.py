'''
def add(x, y=10, z=5):
    a = x + y + z
    return a

print(add(10))

def add_mul(x, y):
    s = x + y
    m = x * y
    i = x - y
    
    return s, m, i

a, b, c = add_mul(20, 4)
print(a, b, c)
'''
print('\\    /\\')
print(' )  ( \')')
print('(  /  )')
print(' \(__)|')

'''
\    /\
 )  ( ')
(  /  )
 \(__)|
'''
numbers = list(range(0, 100, 10))
print(numbers)

import time
while True:
    for i in range(20):
        print(i)
    time.sleep(1)