actual = ['h', 'a', 'j', 'u']
new = ['cssd', 'saw', 'key', 'j']


new = list(filter(lambda email: email not in actual, new))
print(new)