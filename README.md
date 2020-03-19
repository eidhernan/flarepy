# flarepy - a lightweight game engine
Notice - this is **NOT** a framework. This only contains the materials needed to make a game, such as key grabbing, colors, interactive menus, switch/case, and file interaction.
Though, I will provide you with a light framework, for an rpg.

### Requirements
This module has **one** dependency, the [blessed](https://blessed.readthedocs.io/en/latest/) library. It can be installed with a simple ``pip install blessed`` in the terminal.
This dependency has support for color, styling, terminal effects, and more.
### Color
This module has support for color, and it is different from most libraries, in that you can create your own colors... kinda...
You initialize a color object, and it can be used anywhere!
```py
from flarepy import Fp
root = Fp()
red = root.style("red1")
print(red("Hello!"))
```
Will print out "Hello", but in red. Try it out!

If you want to highlight the text instead, prefix the string with "on_".
```py
from flarepy import Fp
root = Fp()
red = root.style("on_red1")
print(red("Hello!"))
```
And if you want a combination, follow the "color_on_highlight" format...
```py
from flarepy import Fp
root = Fp()
red = root.style("black_on_blue1")
print(red("Hello!"))
```
For a list of colors and styles, check [this](https://www.w3schools.com/colors/colors_x11.asp).

### Getting keypresses
Catching keypresses is a bit of a pain in programming, if you decide to work in the terminal. Fortunately, flarepy has a solution for that.
With the ``getkey()`` function, keypresses can be caught. Follow this snippet:
```py
from flarepy import Fp
root = Fp()
while True:
    pressed_key = root.getkey()
    print(pressed_key)
```
The ``getkey()`` method returns the last key pressed. Unfortunately, this may not be what you want, as this pauses the program, and waits for a keypress.
Of course, there is a way to wait for a keypress within a timeout.
```py
from flarepy import Fp
root = Fp()
pressed_key = root.getkey(timeout = 5) #5 seconds
print(pressed_key)
```
This 'timeout' mode changes the wait time for a keypress from infinite, to being limited to n seconds, where n is the value passed for the timeout.
### Menus
With both color and catching keys out of the way, why not have a method which creates an automatic menu?
Well, you don't have to, because it exists. Following the ``menu()`` method, of course:
```py
from flarepy import Fp
root = Fp()
menu_title = "This is a sample title."
menu_contents = {
    "key_1":"Label 1",
    "key_2":"Label 2",
    "key_3":"Label 3"
}
root.menu(menu_title, menu_contents)
```
The title of a menu is the first argument, it must be a string. The contents of a menu must be a dictionary. The key of each item in the dictionary represents the return value of the menu, when the choice is selected, and the value of that key represents what is actually printed out.
Here is an example:
```py
from flarepy import Fp
root = Fp()
menu_title = "This is a sample title."
choice = menu_contents = {
    "key_1":"Label 1",
    "key_2":"Label 2",
    "key_3":"Label 3"
}
print(choice)
```
Do you like the color of the cursor? No? Well, you can change it. Changing the ``menu_style`` property to a valid color will change the color of the cursor for a menu.
Example:
```py
from flarepy import Fp
root = Fp()
red = root.style("red1")
root.menu_style = red
```
Alright, everything seems fine, but something seems missing. 
Oh yeah, the tons of terminal-related stuff. Just read this...
```py
 |  char(character)
 |      Return a character-like object, a string. Can be treated like a string.
 |
 |  clear()
 |      Clear the whole screen.
 |
 |  clear_all()
 |      Return cursor and clear screen
 |
 |  clear_bol()
 |      Clear backward to the beginning of the line.
 |
 |  clear_eol()
 |      Clear to the end of the line.
 |
 |  clear_eos()
 |      Clear to the end of screen.
 |
 |  home()
 |      Sets cursor to (1,1)
 |
 |  move_down(units=1)
 |      Move y characters lelow the current location of the cursor
 |
 |  move_left(units=1)
 |      Move x characters to the left of the cursor
 |
 |  move_right(units=1)
 |      Move x characters to the left of the cursor
 |
 |  move_up(units=1)
 |      Move y characters above the current location of the cursor
 |
 |  move_x(x)
 |      Set the cursor's x position
 |
 |  move_xy(x, y)
 |      Set the xy position of the cursor
 |
 |  move_y(y)
 |      Set the cursor's y position
 |
 |  move_yx(y, x)
 |      Set the yx position of the cursor
 |
 |  sleep(seconds)
 |      sleep, better alternative to SDL's time.sleep()
```
### Switches
If you come from another language, you might me familiar with the switch statement.  flarepy offers a way to emulate switches using function mapping:
```py
from flarepy import Fp
root = Fp()

ctx = 1 #value to be used by the switch

class mySwitch:
    @root.case(1)
    def case1(ctx):
        print("This is case 1.")
        return ctx
    @root.case(2)
    def case2(ctx):
        print("And this is case 2!")
        return ctx
    @root.case("__default__")
    def __default__(ctx):
        print("Case default!")
        return ctx
root.enable(mySwitch, ctx)
```
The ``@case`` decorator marks a function as a case, and the argument passed to the decorator is the condition of the case.
``case 1:`` in Java is equal to ``@root.case(1)`` in flarepy.
And of course, the ``"__default__"`` condition represents the default case of the switch, if the value passed to the switch is not found.
While these are useful, do NOT use this to replace if statements. Simple if statements are always good. This is only really required when you have many conditions that involve long blocks of code.
Wait... why should I tell you what to do?