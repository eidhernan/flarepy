# Abstract
This is a crude finite state machine. It is fast, and it is readable. It uses dict mapping, as well as methods. I am in no way telling anyone to use this, but if you want to, go right ahead.

According to Wikipedia, a finite state machine is an abstract machine that can be in exactly one of a finite number of states at any given time. The FSM can change from one state to another in response to some inputs; the change from one state to another is called a transition.
So technically, this can be categorized as a finite state machine:
```py
def function():
    state = "entry"
    while state != "exit":
        if state == "entry":
            #some commands
            print("Entry state")
            state = "somestate"
        if state == "somestate":
            #some commands
            print("Some state")
            state = "exit"
    print("Finished.")
function()
```
But this is very crude. First of all, whitespace. We have a function, and then we have a while loop, and then we have an if statement in that while loop. And only God knows if there's branching inside a state like this.
It is hard to read as well. This is an obvious violation of PEP8, in terms of whitespace, and with a complicated FSM, endless chains of if statements can get *real* ugly.

Of course, the same can be done with methods. Then again, we can do better. It would be nice if we could have some sort of syntax like this:
```py
def function():
    @state("ENTRY")
    def entry_state():
        print("This is the entry state.")
        state = "ATTACK"

    @state("ATTACK")
    def attack_state():
        print("This is the attack state.")
        state = "EXIT"
```
With this sort of construct, the state machine automatically ends when the state is "EXIT"
This is quite readable, although the decorators may seem redundant at first glance, they are needed.

Unfortunately, this construct isn't entirely possible, because:
1 - These are functions. How could the STATE be passed around?
2 - STATE can't be passed around in classmethods, because classmethods aren't callable.
3 - That means something needs to be returned.

With that, we have this:
```py
from fsm import state, activate, Operations
#Operations.lock = False #Uncomment this if you want?
class StateMachine:
    @state("__main__")
    def __main__(ctx):
        print("This is the first state, moving on to the second state.")
        return "2"
    @state("2")
    def state2(ctx):
        print("This is the second state, moving on to the third.")
        return "3"
    @state("3")
    def state3(ctx):
        print("Third state.")
        return "__exit__"
    @state("__default__")
    def __default__(ctx):
        print("Default state.")
        return "__exit__"
    def __new__(self):
        activate(self)
        return None #Don't create an instance of the class. Therefore, __new__() acts as a way to call the machine.
StateMachine()
```
Now we have a bunch of ``state``s grouped together, with methods defined for each. It does not matter the name for each method, as long as it is unique to the class.
Classes are used to wrap the states into a finite state machine, and the ``__new__`` method contains a single function call, ``activate(self)``. In this case, ``self`` isn't an object, but the class. In essence, when the class is initialized as an object, it is actually called, and a value is returned.
With this, classes can be treated as callables, without initializing them. You do not need to do this, you can simply do ``activate(StateMachine)``, but again, it may seem confusing.
You may also notice how there are returns instead of setting the ``state``. That is because these are methods, and by default, they MUST have some sort of way to pass ``state`` around.
And ``ctx`` is required, it is needed to allow the state to be passed to the function. Of course, since it is decorated, it isn't actually going to the function, but the decorator function. There, the state can be validated.
