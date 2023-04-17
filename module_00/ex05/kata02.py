kata = (2019, 9, 25, 3, 30)

# tuple type and length error handling
assert isinstance(kata, tuple), "TypeError: kata must be a tuple"
assert len(kata) == 5, "ValueError: kata tuple must contain 5 integers"

# Value and Type error handling
for element in kata:
    assert isinstance(element, int), "TypeError: all kata elements must be integers"
    assert element >=0, "ValueError: all kata elements must be non-negative integers"
assert len(str(kata[0])) <=4, "ValueError: kata[0] must containing up to 4 digits"
for element in kata[1:]:
    assert len(str(element)) <=2, "ValueError: kata[1], kata[2], kata[3] and kata[4] must containing up to 2 digits"

# Print date and time contained in kata in a readable format (dd/mm/yyyy hh:mm)
print("{:02d}/{:02d}/{:04d} {:02d}:{:02d}".format(kata[1],kata[2],kata[0],kata[3],kata[4]))
