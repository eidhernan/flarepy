#These are tests designed to check the output of certain operations
from flarepy import Fp
root = Fp()
from blessed import Terminal
t = Terminal()
def styling(style=root.style("red1"), text="Hello World"):
        print(t.gray("STYLING TEST"))
        print()
        print("STYLED STRING: {}".format(style(text)))
        print("RAW STRING: {}".format(repr(text)))
        print("RAW STYLE: {}".format(repr(style.raw_style)))
        print("'READABLE' STYLE: {}".format(repr(style.style)))
        print()
        print(t.gray("PRESS ANY KEY FOR NEXT TEST"))
        root.getkey()
def menus(style=root.menu_style):
    original_style = root.menu_style
    root.menu_style = style
    testcase = root.menu("MENU TEST 1", {"case1":"Case 1.", "case2":"Case 2"})
    if testcase == "case1":
        print(t.clear, end='', flush=True)
        print("Case 1. Press any key to continue.")
        root.getkey()
    if testcase == "case2":
        print(t.clear, end='', flush=True)
        print("Case 2. Press any key to continue.")
        root.getkey()
    root.menu_style = original_style