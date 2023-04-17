kata = "The right format"

# type and length error handling
assert isinstance(kata, str), "TypeError: kata must be a string"
assert len(kata) <= 42, "ValueError: kata string's length must not be higher than 42"


# Make the kata variable always a string whose length is not higher than 42
# if longer, we slice it. Else, we fill it with '-' chars to make it 42 chars long
if len(kata) > 42:
    kata = kata[:42]
else:
    kata = "-"*(42-len(kata)) + kata
print(kata, end='')