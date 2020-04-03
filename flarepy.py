import re
import pickle
from blessed import Terminal
t = Terminal()

def raw_print(string):
    print(string, end='', flush=True)

class CharLengthError(Exception):
    """A character is too long"""
    __module__ = Exception.__module__
    def __init__(self):
        default_message = "'char' class must consist of one character." 
        super().__init__(default_message)


class char:
    """Character-like object, a string"""
    def __init__(self, char):
        if type(char) == str:
            if len(char) == 1:
                self.__value = char
            else:
                raise CharLengthError()
        else:
            raise TypeError("'char' class must be wrapped in quotes.")
    def e(self):
        return "A"
    def __repr__(self):
        return repr(self.__value)
    def __str__(self):
        return self.__value
    def __eq__(self, other):
        return other == self.__value
    def __ne__(self, other):
        return other != self.__value
    def __add__(self, other):
        return self.__value + other
    def __radd__(self, other):
        return (self.__value + other)
    def upper(self):
        return self.__value.upper()
    def lower(self):
        return self.__value.lower()
class classproperty(object):
    """@property, but for classes, not instances"""
    def __init__(self, pointer:any):
        self.pointer = classmethod(pointer)
    def __get__(self, *a):
        return self.pointer.__get__(*a)()

class Style(str):
    """Allow the creation of styles"""
    def __init__(self, style:str) -> str:
        self.style:str = style
        self.raw_style = getattr(t, style)
    def __apply__(self, string:str) -> str:
        """Apply the style to a string"""
        return self.raw_style(string)
    def __repr__(self) -> str:
        return repr(self.raw_style)
    def __str__(self) -> str:
        return self.raw_style
    def __call__(self, string:str) -> str:
        """Gateway to __call__()"""
        return self.__apply__(string)
class Utility:
    """Utility methods, used for general things"""
    @staticmethod
    def strip_ansi(string:str) -> str:
        """Remove ANSI escape codes from a string, leaving behind just text"""
        return re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('', string) 
    @classmethod
    def splitstring(cls, string:str, length:int):
        """Split string by words, and by line number. Length is the width of the t."""
        newstr = cls.strip_ansi(string).splitlines()
        newstr1 = []
        for string in newstr:
            newstr1.extend([string[i:i+length] for i in range(0, len(string), length)])
        return newstr1
    
    
    @staticmethod
    def ms(milliseconds:int) -> float:
        """convert milliseconds to seconds"""
        return milliseconds/1000
    @staticmethod
    def strip_string(string:str, query:str) -> str:
        """Remove word from string"""
        if query:
            while string.startswith(query):
                string = string[len(query):]
            while string.endswith(query):
                string = string[:-len(query)]
        return string
    @staticmethod
    def dict_to_object(obj, dict):
        """Store the values of a dictionary as the attributes of a passed object"""
        for item in dict.items():
            setattr(
                obj,
                item[0],
                item[1]
            )




class Fp:
    def __init__(self):
        self.__width = t.width
        self.__height = t.height
        self.case = case
        self.enable = enable
        self.queue = []
    @staticmethod
    def char(character):
        """Return a character-like object, a string. Can be treated like a string."""
        return char(character)
    @property
    def width(self):
        """Returns the width of the terminal"""
        return self.__width
    @width.setter
    def width(self, value):
        raise AttributeError("'width' property can't be changed.")
    @width.deleter
    def width(self):
        raise AttributeError("'width' property can't be deleted.") 
    @property
    def height(self):
        """Returns the height of the terminal"""
        return self.__height
    @height.setter
    def height(self, value):
        raise AttributeError("'height' property can't be changed.")
    @height.deleter
    def height(self):
        raise AttributeError("'width' property can't be deleted.")
    @staticmethod
    def getkey(timeout = None):
        """Pauses the program, and waits for the user to press a key. That key is returned. There is an optional timeout argument, which requires the user to press a key before the timeout ends."""
        with t.cbreak():
            value = t.inkey(timeout = timeout)
        if value.is_sequence:
            fin = value.name
        elif value == '':
            fin = None
        elif value == ' ':
            fin = "KEY_SPACE"
        else:
            fin = char(str(value))
        
        return fin
    @staticmethod
    def sleep(seconds):
        """sleep, better alternative to SDL's time.sleep()"""
        with t.cbreak():
            t.inkey(timeout=seconds)
    @staticmethod
    def move_up(units = 1):
        """Move y characters above the current location of the cursor"""
        raw_print(t.move_up(units))

    @staticmethod
    def move_down(units = 1):
        """Move y characters lelow the current location of the cursor"""
        raw_print(t.move_down(units))

    @staticmethod
    def move_left(units = 1):
        """Move x characters to the left of the cursor"""
        raw_print(t.move_left(units))

    @staticmethod
    def move_right(units = 1):
        """Move x characters to the left of the cursor"""
        raw_print(t.move_right(units))

    @staticmethod
    def move_x(x):
        """Set the cursor's x position"""
        raw_print(t.move_x(x))
    
    @staticmethod
    def move_y(y):
        """Set the cursor's y position"""
        raw_print(t.move_y(y))
    
    @staticmethod
    def move_xy(x, y):
        """Set the xy position of the cursor"""
        raw_print(t.move_xy(x, y))
    
    @staticmethod
    def move_yx(y, x):
        """Set the yx position fo the cursor"""
        raw_print(t.move_xy(y, x))
    
    @staticmethod
    def home():
        """Sets cursor to (1,1)"""
        raw_print(t.home)
    
    @staticmethod
    def clear():
        """Clear the whole screen."""
        raw_print(t.clear)
    
    @staticmethod
    def clear_eol():
        """Clear to the end of the line."""
        raw_print(t.clear_eol)
    
    @staticmethod
    def clear_bol():
        """Clear backward to the beginning of the line."""
        raw_print(t.clear_bol)
    
    @staticmethod
    def clear_eos():
        """Clear to the end of screen."""
        raw_print(t.clear_eos)
    @staticmethod
    def clear_all():
        """Return cursor and clear screen"""
        raw_print(t.clear + t.home)
    @property
    def menu_style(self):
        """The style of the cursor, in menus"""
        return Menu.highlight_style
    @menu_style.setter
    def menu_style(self, style):
        Menu.highlight_style = style
    @menu_style.deleter
    def menu_style(self):
        raise AttributeError("can't delete attribute.")
    @staticmethod
    def menu(title:str, contents: dict):
        """Generate a menu. """
        return Menu.menu(title, contents)
    @staticmethod
    def style(style):
        """Create a style object."""
        return Style(style)
    @classmethod
    def wait_for_keys(cls, keys):
        """Wait for a key in a list of keys to e pressed"""
        pressed_key = ''
        while pressed_key not in keys:
            pressed_key = cls.getkey()
        return pressed_key

    @classmethod
    def wait_for_key(cls, key):
        """Wait for a specified key to be pressed"""
        pressed_key = ''
        while key != pressed_key:
            pressed_key = cls.getkey()
        return pressed_key
    #empty list...
    def queue_append(self, object):
        """Append an object to the queue."""
        self.queue.append(object)
    def queue_remove(self, object):
        """Remove an object from the queue"""
        self.queue.remove(object)
    
    def queue_clear(self):
        """Wipe the queue"""
        self.queue = []
    
    def queue_dump(self, filename):
        """Dump the contents of the queue to a file. The queue must be manually cleared after this"""
        if self.queue == []:
            raise AttributeError("queue is empty")
        with open(filename, "wb") as f:
            pickle.dump(
                obj = self.queue,
                file = f
            )
    
    @staticmethod
    def object_dump(object, filename):
        """Dump a single object to a file"""
        with open(filename, "wb") as f:
            pickle.dump(
                obj = object,
                file = f
            )
    
    @staticmethod
    def raw_load(filename):
        """Load a raw file to an object"""
        with open(filename, "rb") as f:
            return pickle.load(file = f)

    @staticmethod
    def load_as_object(filename, obj):
        """Load a dictionary-serialized file to an object."""
        with open(filename, "rb") as f:
            dict = pickle.load(file = f)
        Utility.dict_to_object(obj, dict)
class Menu:
    """Generate a menu"""
    highlight_style = Style("gold1")
    @classmethod
    def menu(cls, title, contents, delay=Utility.ms(27)):
        Fp.getkey(timeout = Utility.ms(27))
        print(t.home + t.clear, end='', flush=True)
        if type(contents) != dict:
            raise TypeError("Menu contents must be a dict.")
        with t.cbreak(): #event loop
            cursor_position = 1
            print(title)
            titlelen = Utility.splitstring(title, t.width)
            while True:
                print(t.move_y(len(titlelen)), end='', flush=True)
                current_iter = 0
                for item in contents.items():
                    current_iter += 1
                    if current_iter == cursor_position:
                        print("  " + str(cls.highlight_style(item[1])), flush=True)
                        selected_choice = item[0]
                    elif current_iter != cursor_position:
                        print("  " + str(item[1]), flush=True)
                del item
                pressed_key = Fp.getkey()
                if pressed_key == "KEY_UP":
                    if cursor_position == 1:
                        cursor_position = len(contents)
                    elif cursor_position != 1:
                        cursor_position -= 1
                elif pressed_key == "KEY_DOWN":
                    if cursor_position == len(contents):
                        cursor_position = 1
                    elif cursor_position != len(contents):
                        cursor_position += 1
                elif pressed_key in ["KEY_ENTER", "Z".lower()]:
                    return selected_choice
