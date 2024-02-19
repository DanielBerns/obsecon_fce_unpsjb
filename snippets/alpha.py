# https://madebyme.today/blog/python-dict-vs-curly-brackets/

import dis

def a():
  return dict()

def b():
  return {} 

def c():
  return list()

def d():
  return []

print('\n\n')
print('a code')
dis.dis(a)

print('\n\n')
print('b code')
dis.dis(b)

print('\n\n')
print('c code')
dis.dis(c)

print('\n\n')
print('d code')
dis.dis(d)
