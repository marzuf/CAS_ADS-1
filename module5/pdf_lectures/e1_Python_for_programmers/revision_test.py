# General introduction

#> "_" holds the last previous result
x = 5
x+2
_ + 3 # -> returns 10
print(_)

# 1.	Flow control tools

# use of else in the for loop

for i in range(1, 10):
    for j in range(1,10):
        if j == 3:
            print("hello")
            break
    else:
        print(i)
# => used to make the code clearer after a "break" statement
# (NB: if no break before: no error but does not make sense...

def this_function():
    pass
is_this_none = this_function()

is_this_none == None
# True


# function annotation
def my_func(ham :str, eggs :str= "eggs") -> str :
	print(my_func.__annotations__)
	print(ham + " - " + eggs)

my_func(ham="hello")
# {'ham': <class 'str'>, 'eggs': <class 'str'>, 'return': <class 'str'>}
# hello - eggs


# 2.	Generators

def gen_ten():
    yield from range(1,10)

a = gen_ten()
next(a)

# 3.	Comprehensions with lists

# 4.	Comprehensions with dicts

# 5.	Comprehensions with sets

# 6.	Creation of classes

# 7.	Context managers

# 8.	Code debugging using pdb package

# 9.	Introspection of objects with introspect module

# 10.	Virtual environments

# 11.	Develop Python packages

# 12.	Script/application entry point (__main__)
