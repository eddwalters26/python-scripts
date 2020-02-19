def fizzBuzz(uptoValue, mod1, mod2):
    for i in range(uptoValue):
        if i % mod1 == 0 and i % mod2 == 0:
            i = "FizzBuzz"
        elif i % mod1 == 0:
            i = "Fizz"
        elif i % mod2 == 0:
            i = "Buzz"
        print(i)

fizzBuzz(100, 3, 5)
