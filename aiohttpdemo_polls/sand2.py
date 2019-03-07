import re

a = re.match(r'2015-..-..', '2014-12-15 15:30:51.234+02')
print(a)
if a != None:
    print(True)
else:
    print(False)