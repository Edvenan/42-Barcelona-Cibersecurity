kata = "The right format"

# Make the kata variable always a string whose length is not higher than 42
# if longer, we slice it. Else, we fill it with '-' chars to make it 42 chars long
if len(kata) > 42:
    kata = kata[:42]
else:
    kata = "-"*(42-len(kata)) + kata
print(kata, end='')