kata = (19,42,21)

# Store as strings all integers in kata in a new list
nums = []
for num in kata:
    nums.append(str(num))

# Print number of items in kata and each item separated by comma
print(f"The {len(kata)} numbers are:",", ".join(nums))