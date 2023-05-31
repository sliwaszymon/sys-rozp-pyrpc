import time
from pyRpc import PyRpc
import sympy as sp

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

def _calculate_delta(expression):
    x = sp.symbols('x')
    delta = sp.simplify(expression).as_poly(x).discriminant()
    return delta
 
 
def _calculate_roots(expression):
    x = sp.symbols('x')
    delta = _calculate_delta(expression)
    if delta < 0:
        return None
    elif delta == 0:
        x_val = sp.solve(expression, x)[0]
        return x_val
    else:
        x_vals = sp.solve(expression, x)
        return x_vals
 
 
def square_function(expresion):
    """ Returns delta and roots of square function 
    	example input: "x**2 + 2*x + 2" """
    return (_calculate_delta(expresion), _calculate_roots(expresion))
 

def simplify_function(expresion):
    """ Returns simplified version of given function 
    	example input: "x**2 + 2*x" """
    return sp.simplify(expresion)
 
 
def calculate_integral(expresion):
    """ Calculates integral of given function
		example input: "x**2 + 2*x" """
    return sp.integrate(expresion)

def calculate_derivative(expresion):
    """ Calculates derivative and double derivative of given function
		example input: "x**2 + 2*x" """
    f_prime = sp.diff(expresion)
    f_double_prime = sp.diff(f_prime)
    return (f_prime, f_double_prime)



myRpc = PyRpc("pl.UWMWMII.pyRpcCalculator") 
time.sleep(.1)

myRpc.publishService(add)
myRpc.publishService(substract)
myRpc.publishService(multiplicate)
myRpc.publishService(devide)
myRpc.publishService(pow)
myRpc.publishService(root)
myRpc.publishService(square_function)
myRpc.publishService(simplify_function)
myRpc.publishService(calculate_integral)
myRpc.publishService(calculate_derivative)

myRpc.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    myRpc.stop()
    