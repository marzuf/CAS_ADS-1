import numpy


# !!! in python3, division always returns a float !
# to have int as return (floor division): use double division sign: //
# NB: -17 // 6 = -3 but 17//6 = 2 => floor

# "_" => the previous output, e.g.

x = 5
x+2
_ + 3 # returns 10


print("some \name")  # here \n means newline
print(r"some \name") # here \n interpreted as std characters

3*'Py'  # 'PyPyPy'

'Py' 'thon'  # will concatenate the string (does not work with variables)


word = "python"
word[:42]  # => this will not raise an error !! will print 'python'
#word[42] # => this will raise an error but:
word[41:42] # => slice does not return error, this will return ''
#word[0] ='j'  # strings are immutable !!!

a, b = 0, 1
# => this creates tuple to assign values to the variables

# you can change the end character used by print
# (default is a newline)
print(a, end = ',')


numbers = list(range(4))
numbers.index(3)  # to retrieve the index of list element

myletters = ['a','b','c','d']

for i, let in enumerate(myletters):
    print(str(i) + "\t" + let)


# better not to use break (inreadable !, not pythonic)


# the for loop has an else statement !!!
#
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        #...         # loop fell through without finding a factor
        print(n, 'is a prime number')

# more explicit to use
# will not change the flow of the code

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
        #...         # loop fell through without finding a factor
        print(n, 'is a prime number')
# 'pass' statement => does nothing

def this_function():
    pass
is_this_none = this_function()

is_this_none == None
True
# return type of pass is None
# => usage: can be more explicit to use a function that ends with "pass" rather than return None


# no scope, variables available outside functions !

i = 5

def f(arg=i):
    print(arg)
i = 6
f()
# will print 5 !!!
# when f() is defined, i = 5, so it will print 5

def f(a, L=[]):
    L.append(a)
    return L
print(f(1)) # [1]
print(f(2)) # [1,2]
print(f(3)) # [1,2,3]


# rather never assign empty list as argument
#L is immutable, stores a reference

# better to define it as none
def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L


def keyword_args(*, without_def, with_def='def'):
    pass

# force the user to use keyword args
# without the star, without_def can be used as position argument
# if someone switch the two first arguments and you give the first two
# without keyword, it will still work, so it could be better to force using keyword arguments
# the value of * is not stored, syntaxic sugar !

# keyword_args('a')
# error, taken as positional arguments, argument for without_def
# useful: add a star, so you are forced to call function with keyword arguments changed
# (using the star, you can know if you change the names of keyword arguments !)

# keyord_args(with_def='a') # will not work, value for without_def is missing

keyword_args(without_def='a')
#  => will work


def kwargs_func(*args, **kwargs):
    print(kwargs['test']) # print the 'test' kwargs argument

# can be handy but dangerous because does not test the name of the arguments
# kwargs_func(tset = 'tset')
# will be accepted as an argument, but will crash !

#lambda expression -> have a function without using function name

# function annotations:
def f(ham:str, eggs:str='eggs') -> str:
    print(f.__annotations__)
print("hello")
print(1)
# => are useful for documentation,
# but will not be used by the interpreter (will not crash if you don't pass the good type)


# GENERATORS
# function that allows to return values from time to time and then continue computation
# use of "yield" statement

def reverse(data):
        for index in range(len(data)-1,-1,-1):
            yield data[index]

for char in reverse("golf"):
    print(char)
# e.g. to iterate over a match to do something over everything that matches

# useful for iterating over the elements

# yield statement used in generators
# different than return, because will continue up where it is stopped when function called again

def fibonacci(limit=100):
    a,b = 0,1
    while a < limit:
        yield a         # return the a value
        a,b = b,a + b

fib = fibonacci(10)
next(fib) # 0
next(fib) # 1
next(fib) # 1
next(fib) # 2
# to restart at 0 -> recall fib = fibonacci(10)
fib = fibonacci(10)
next(fib) # 0
next(fib) # 1

for fib in fibonacci(10):
    print(fib)


fib = fibonacci(3)
next(fib)
next(fib)
next(fib)
next(fib)
# next(fib) # error: StopIteration exception -> the for loop knows when to end
# next calls fib.__next()__

# => inside of huge one-liners
squares = [
    number ** 2
    for number in range(10)
    if not number % 2
    ]

# you can do dict comprehension as well
# and also set comprehension (using {} instead of [] )



### CLASS

class MyClass:
    i = 12345

    def f(self):
        return("hello world")

# constructor
# 2 different construcotrs: nwe and init
# usually we use init
# to give some initial values: define __init__

# def __init__(self):
# self is the instance of the object
# you don't a "this" like in java, should be passed in the method
# convention to name it 'self' but could be any name

# you can always access all the variables (there is no public or private)
# but if start with _ or __ => convention to use it internal of the classes
# (but still could always be accessed)

# variables defined outside the __init__ function
# if you change the class variables -> will be changed for  all class variable

x = MyClass()
x.i

z = MyClass()
z.i = 8910
x.i # ?? still returns 12345

MyClass().i = 8910
x.i # ?? still returns 12345


# will call the super of the first class that matches (that has a init function defined)

class Mixin:
    def __init__(self):
        print('mixin')

class BaseClass:
    def __init__(self):
        print('base')

class SubClass(Mixin, BaseClass):
        def __init__(self):
            super().__init__()
SubClass()
# mixin
# the Mixin init is called
# if you call a super, will call the 1st that match
# so in general for the inherited classes, you don't define the init
# so that BaseClass constructor will be called instead
# goes from left to right, and when find a matching for super() will call this constructor

# iter function if next function

### CONTEXT MANAGER

# define a piece of logic before doing something or after finishing doing something
# e.g. doing sth when a file is closed
# -> with statement

# __enter()__ and __exit()__

# when you call with the with

with open('test', 'r') as test_file:
    print(test_file.read())

## DEBUGGING
# package pdb
# you can trace the error, stop whenever you want

import pdb
pdb.set_trace() # => allows to stop everywhere you want

# when you hit the trace call, you enter pdb, and a set of commands is available
# cf documentation for description of all available functions
# (e.g. you can run next statement)
# when it enters in Pdb mode, you can access the internal variables
# go through every step up to the error to see where error comes from

# inspect module
# check the call, look at the signature of the method
import inspect
# helpful when you are doing introspection (if of a given type do that, otherwise do this, etc., etc.)
# inspect is useful when you expect some specific variable types

### PACKAGES
# in principle, should never be needed to sudo pip install

# venv module
# create a virtual environment, only things installed inside this environment will be used during runtime

# IN THE COMMAND LINE
#mkdir /tmp/another_tmp
#cd /tmp/another_tmp
#python3 -m venv .    # this creates some files and folders
#source bin/activate # everything run will be run inside virtual environments
#pip install fahrplan # -> install the package locally, will be located in the bin folder

# NB: j command

# CREATE PFP PACKAGE

# create a pfp folder that will be our package

# edit setup.py [copy path from python website]
# add:
# #!/usr/bin/env python
# remove some useless lines

# smallest possible package pfp file
import setuptools

# touch pfp/__init__.py
#= indicates to python that this folder is a package

# pip install -e .
#  -e use witout reinstallation
# pfp.egg-link => path to where the packages are installed,
# python knows how and where to access folders and packages

# 1) game of life; 3 living cells surrounded remain, if more die

########################## practical of the afternoon

# see notes.txt

