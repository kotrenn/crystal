from craftparser import *

parser = CraftParser()

parser.open('craft.txt')
recipes = parser.read()
parser.close()

print ''
for recipe in recipes:
    print recipe
