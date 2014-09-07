from recipeparser import *

parser = RecipeParser()

parser.open('recipes.txt')
recipes = parser.read()
parser.close()

print ''
for recipe in recipes:
    print recipe
    print ''
