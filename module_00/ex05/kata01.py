kata = {
'Python': 'Guido van Rossum',
'Ruby': 'Yukihiro Matsumoto',
'PHP': 'Rasmus Lerdorf',
}

# Print each key:value pair in kata
for key, value in kata.items():
    print("{} was created by {}".format(key, value))