import flarepy
from statemachine import state, activate
root = flarepy.Fp()
red = root.style("red1")

class TitleScreen:
    @state("__main__")
    def __main__(ctx):
        controls = "Controls:\n\nArrow Keys: Navigate menus\nEnter: Confirm selection."
        root.clear_all()
        print(controls)
        root.getkey()
        return "title_menu"

    @state("title_menu")
    def title_menu(ctx):
        return root.menu(
            title=red("Your game title."),
            contents = {
                "new_game":"New game",
                "continue":"Continue",
                "credits":"Credits",
                "quit":"Quit"
            }
        )
    @state("new_game")
    def new_game(ctx):
        root.clear_all()
        print("Not implemented, sending user back to title...")
        root.sleep(2)
        return "title_menu"
    @state("continue")
    def continue_game(ctx):
        root.clear_all()
        print("Not implemented, sending user back to title...")
        root.sleep(2)
        return "title_menu"
    @state("credits")
    def credits(ctx):
        root.clear_all()
        print("Engine and demo made by DH93. If you want to use this engine, you MUST credit me. (=")
        root.getkey()
        return "title_menu"
    @state("quit")
    def quit(ctx):
        return root.menu(
            title="Are you sure you want to quit?",
            contents={
                "__exit__":"Yes","title_menu":"No"
            }
        )
    def __init__(self):
        activate(type(self))


if __name__ == "__main__":
    TitleScreen()
else:
    TitleScreen()