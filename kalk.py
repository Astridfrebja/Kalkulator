def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    return a ** b

a = float(input('Første tall: '))
b = float(input('Andre tall: '))

funksjon = input('Skriv funksjon: "+", "-", "/", "*", "^": ')

if funksjon == "+": 
    print('Svar: ', add(a, b))
elif funksjon == "-":
    print('Svar: ', subtract(a, b))
elif funksjon == "/":
    print('Svar: ', divide(a, b))
elif funksjon == "*":
    print('Svar: ', multiply(a, b))
else:
    print('Svar: ', power(a, b))