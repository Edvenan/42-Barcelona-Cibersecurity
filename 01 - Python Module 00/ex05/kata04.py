kata = (0, 4, 132.42222, 10000, 12345.67)

# tuple type and length error handling
assert isinstance(kata, tuple), "TypeError: kata must be a tuple"
assert len(kata) == 5, "ValueError: kata tuple must contain 5 integers"

# Value and Type error handling
assert isinstance(kata[0], int), "TypeError: kata[0] must be a non-negative integer containing up to 2 digits"
assert kata[0] >= 0 and len(str(kata[0])) <=2, "ValueError: kata[0] must be a non-negative integer containing up to 2 digits"

assert isinstance(kata[1], int), "TypeError: kata[1] must be a non-negative integer containing up to 2 digits"
assert kata[1] >= 0 and len(str(kata[1])) <=2, "ValueError: kata[1] must be a non-negative integer containing up to 2 digits"

assert isinstance(kata[2], float), "TypeError: kata[2] must be a decimal(float)"

assert isinstance(kata[3], int), "TypeError: kata[3] must be an integer"

assert isinstance(kata[4], float), "TypeError: kata[4] must be a decimal(float)"


# Print tuple contents in different numerical formats
print("module_{:02d}, ex_{:02d} : {:,.2f}, {:,.2e}, {:,.2e}".format(kata[0],kata[1],kata[2],kata[3],kata[4]))