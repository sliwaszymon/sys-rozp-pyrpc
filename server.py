import time
from pyRpc import PyRpc

def add(a, b):
	""" Returns result of sum a + b """
	return a + b

def substract(a, b):
	""" Returns result of substraction a - b """
	return a - b

def multiplicate(a, b):
	""" Returns result of multiplication a * b """
	return a * b

def devide(a, b):
	""" Returns result of division a / b """
	return a / b

def pow(a, b):
	""" Returns result of a to power of b """
	return a ** b

def root(a, b):
    """ Returns result of a roots of b """
    return a ** (1 / b)


myRpc = PyRpc("pl.UWMWMII.pyRpcCalculator") 
time.sleep(.1)

myRpc.publishService(add)
myRpc.publishService(substract)
myRpc.publishService(multiplicate)
myRpc.publishService(devide)
myRpc.publishService(pow)
myRpc.publishService(root)

myRpc.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    myRpc.stop()
    

#problem
#jak rozwiązaliśmy
#bibliografia