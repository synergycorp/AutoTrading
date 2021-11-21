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