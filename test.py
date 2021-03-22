a = ["hello", "bye"]
b = set()
b.update(a)
a = {"hello"}
b.symmetric_difference_update(a)
print(b)
