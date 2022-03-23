import os
import sys


current = os.getcwd()
dir_name = os.path.dirname(current)
print(current)
print(dir_name)
os.chdir(dir_name)

f = open('te.txt', 'r')
print(f.readlines())
f.close()
