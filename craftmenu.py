from recipeparser import *
from recipeviewer import *
from menu import *

class CraftMenu(Menu):
    def __init__(self, parent, player):
        parser = RecipeParser()
        parser.open('recipes.txt')
        recipes = parser.read()
        parser.close()

        recipe_names = [recipe.label for recipe in recipes]
        Menu.__init__(self, parent, recipe_names + ['Quit'])
        self.recipes = recipes
        self.player = player

    def select(self, msg):
        if msg == 'Quit':
            self.exit()

        for recipe in self.recipes:
            if msg == recipe.label:
                self.child = RecipeViewer(self, recipe, self.player)
