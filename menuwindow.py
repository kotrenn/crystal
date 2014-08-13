class MenuWindow(Window):
    def __init__(self, parent, menu):
        Window.__init__(self, parent)
        self.menu = menu

    def display(self, dst):
        self.menu.display(dst)
