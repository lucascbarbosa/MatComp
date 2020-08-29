a = list(range(10))
print(list(filter(lambda x: x if x%4!=0 else None,a)))