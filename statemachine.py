class Operations:
    lock = True

class MissingReturnError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__suppress_context__ = True

class StateNotFound(Exception):
    """Used to communicate with __call__(), in the helper decorator, to indicate that no matching state following the criteria has been found.
    When this happens, the machine moves on to the next iteration.
    """
    pass
class StateFound(Exception):
    """The state has been found in the current iteration."""
    pass
class _State(object):
    """Helper decorator"""
    def __init__(self, function, state=None):
        self.function = function
        self.state = state

    def __call__(self, ref, *args):
        if ref == self.state:
            ref1 = self.function(ref, *args)
            StateFound.msg = ref1
            raise StateFound(ref1)
        else:
            raise StateNotFound(ref)
def state(condition):
    def state_factory(function=None):
        """ 
        Decorator, used to indicate a state inside a machine.
    
        The user may pass any keyword argument in, as the reference value, but it cannot be a positional one.
    
        Parameters: 
            ?: The value, used to compare with the reference.    
        """
        if function:
            return _State(function, condition)
        else:
            def wrapper(function):
                return _State(function, condition)
            return wrapper
    return state_factory

@state
def _() -> None:
    """This function is used to set the @state decorator"""
    return None
def copyEnable(machine, ref, expected):
    """A copy of the enable method, used to call the Operations.Default fallback state method in a machine."""
    for thing in machine.__dict__:
        #print("{}  :  {}".format(thing, machine.__dict__[thing]))
        if isinstance(machine.__dict__[thing], _State):
            try:
                machine.__dict__[thing](ref)
            except StateNotFound:
                continue
            except StateFound:
                return StateFound.msg
    return expected
def enable(machine: type, ref: any) -> object:
    """ 
    Activate a machine class.
  
    This allows the user to 'enter' the machine.
  
    Parameters: 
        machine (class): A class, representing a machine.
        ref (any): The value that the machine compares its cases to.
    
    Returns: 
        ref: The reference, this value is returned to allow the reference to be altered from within a state, therefore creating a dynamic state machine, if encased within a loop.
    """
    for thing in machine.__dict__:
        if isinstance(machine.__dict__[thing], _State):
            try:
                machine.__dict__[thing](ref)
            except StateNotFound:
                if ref != None:
                    Operations.Default = True
                StateFound.msge = ref
            except StateFound:
                Operations.Default = False
                if ref != None:
                        StateFound.fallmsg = ref
                return StateFound.msg
    expectedReference = ref
    if Operations.Default:
        return copyEnable(machine, ref="__default__", expected = expectedReference) 
    else:
        raise MissingReturnError("State '{}' in machine '{}' missing a return statement, or it returns None..".format(StateFound.fallmsg, machine.__name__))
def activate(machine):
    """Activate the state machine."""
    state = '__main__'
    itere = 0
    while state != "__exit__":
        itere += 1
        state = enable(machine, state)
        if itere == 32767 and Operations.lock == True:
            rmsg = "manual.\n\nRuntimeError: state machine iteration capacity (32767) exceeded, expected state '{}'.\n\nIf this was expected, set 'Operations.lock' to False. Otherwise, try adding a default state to your machine.".format(state)
            raise Exception(str(rmsg)) from None