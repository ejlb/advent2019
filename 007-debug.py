output = 0

def f():
    while True:
        x = yield
        yield x*2

gen = f()
next(gen)

for i in range(101):
    output = gen.send(i)
    print(output)
    next(gen)
