import time
from pyRpc import RpcConnection
	 
remote = RpcConnection("pl.UWMWMII.pyRpcCalculator")
time.sleep(.1)

def add(a, b):
    resp = remote.call('add', args=(a, b))
    print(f'Result of {a} + {b} is {resp.result}')

def substract(a, b):
    resp = remote.call('substract', args=(a, b))
    print(f'Result of {a} - {b} is {resp.result}')

def multiplicate(a, b):
    resp = remote.call('multiplicate', args=(a, b))
    print(f'Result of {a} * {b} is {resp.result}')

def devide(a, b):
    resp = remote.call('devide', args=(a, b))
    print(f'Result of {a} / {b} is {resp.result}')

def pow(a, b):
    resp = remote.call('pow', args=(a, b))
    print(f'Result of {a} to the power of {b} is {resp.result}')

def root(a, b):
    resp = remote.call('root', args=(a, b))
    print(f'Result of {a} roots of {b} is {resp.result}')

def square_function(expression):
    resp = remote.call('square_function', args=[expression])
    if resp.result[0] < 0:
        print(f'Delta of {expression} is {resp.result[0]} so there are no roots.')
    elif resp.result[0] == 0:
        print(f'Delta of {expression} is {resp.result[0]} so there is one root: {resp.result[1]}.')
    else:
        print(f'Delta of {expression} is {resp.result[0]} so the roots are: {resp.result[1][0]} and {resp.result[1][1]}')

def simplify_function(expresion):
    resp = remote.call('simplify_function', args=[expresion])
    print(f'Simplified version of expresion {expresion} is {resp.result}')

def calculate_integral(expresion):
    resp = remote.call('calculate_integral', args=[expresion])
    print(f'Integral of expresion {expresion} is {resp.result}')

def calculate_derivative(expresion):
    resp = remote.call('calculate_derivative', args=[expresion])
    print(f'For expresion {expresion} we have:')
    print(f'Derivative: {resp.result[0]}')
    print(f'Double derivative: {resp.result[1]}')

def help():
    resp = remote.availableServices()
    print('\n===== Available services =====\n')
    for service in resp.result:
        print('Service: %(service)s \nDescription: %(doc)s \nUsage: %(format)s\n' % service)
    print("==============================\n")

listen = True
print('Welcome in PyRpc calculator')
print('If you need help type "help"')
print('To exit program type "exit"\n')
while listen:
    command = str(input('$ '))
    if command == 'exit':
        listen = False
        break
    if command == 'help':
        help()
    elif command.split('(')[0] in [service['service'] for service in remote.availableServices().result]:
        exec(command)
    else:
        print('Service does not exist or you entered the command incorrectly.')
    time.sleep(1)

remote.close()

time.sleep(1)