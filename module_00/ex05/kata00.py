kata = (19,42,21)

nums = []
for num in kata:
    num = str(num)
    nums.append(num)

print(f"The {len(kata)} numbers are:",", ".join(nums))