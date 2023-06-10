kata = {
'Python': 'Guido van Rossum',
'Ruby': 'Yukihiro Matsumoto',
'PHP': 'Rasmus Lerdorf',
}

# Value and Type error handling
assert isinstance(kata, dict), "TypeError: kata must be a dictionary"
for k,v in kata.items():
    assert isinstance(k, str), "TypeError: all kata keys must be strings"
    assert isinstance(v, str), "TypeError: all kata values must be strings"

# Print each key:value pair in kata
for key, value in kata.items():
    print("{} was created by {}".format(key, value))