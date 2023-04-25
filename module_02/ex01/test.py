def myfunc(a):
  return len(a)


a = 4
b = ("Jenny", "Christy", "Monica")
c = ("Monica", "Jenny", "Christy", "Ally")

x = ft_map(myfunc, ('apple', 'banana', 'cherry'))
y = ft_map(lambda x,y,z: x+y+z, ('apple', 'banana', 'cherry'),['apple', 'banana', 'cherry'],"KAS")
z = ft_map(lambda x,y,z: x+y+z, b, 4)

print(list(x))   
print(list(y))
print(list(z))


num1 = [4, 5, 6]
num2 = [5, 6, 7]

result = ft_map(lambda n1, n2: n1+n2, num1, num2)
print(list(result))


a = 4
b = ("Jenny", "Christy", "Monica")
c = ("Monica", "Jenny", "Christy", "Ally")

def myfunc():
    return 4
ft = ft_map(myfunc, 6, 4)
#st = map(3,6,9)
print(list(ft))

'''    
Examples
# Example 1:
x = [1, 2, 3, 4, 5]
ft_map(lambda dum: dum + 1, x)
# Output:
<generator object ft_map at 0x7f708faab7b0> # The adress will be different

list(ft_map(lambda t: t + 1, x))
# Output:
[2, 3, 4, 5, 6]

# Example 2:
ft_filter(lambda dum: not (dum % 2), x)
# Output:
<generator object ft_filter at 0x7f709c777d00> # The adress will be different

list(ft_filter(lambda dum: not (dum % 2), x))
# Output:
[2, 4]

# Example 3:
lst = [’H’, ’e’, ’l’, ’l’, ’o’, ’ ’, ’w’, ’o’, ’r’, ’l’, ’d’]
ft_reduce(lambda u, v: u + v, lst)
# Output:
"Hello world"

'''