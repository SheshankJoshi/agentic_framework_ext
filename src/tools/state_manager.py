"""
This module provides utilities for wrapping functions with dynamic state.
In particular, it provides a decorator factory to wrap a factory function that returns
a function which closes over certain state variables. These state variables can be altered
temporarily and then restored using a context manager pattern.

The provided utilities are:

- stateful_function(factory_fn): 
    A decorator that wraps a factory function, extracting closure variables (state)
    and providing functions to update, get, or temporarily modify these states via a context manager.

- StateContext:
    A context manager that accepts multiple pairs of (stateful function, desired temporary state)
    and ensures that each function's state is updated for the duration of a context, then automatically restored.
"""

from contextlib import contextmanager, ExitStack
from functools import partial

def stateful_function(factory_fn):
    """
    A decorator for stateful functions.
    
    This function wraps a factory_fn that returns a function with closure variables.
    The purpose is to extract these closure variables and provide mechanisms to change
    the state by:
      - set_state: Directly setting the state of any variable in the closure.
      - state: A context manager that temporarily changes state variables, automatically 
          restoring them after the context ends.
      - get_state: Retrieving the current state of all closure variables.

    Raises:
        ValueError: If the returned function does not have any closure variables.

    Returns:
        A new version of the function with added attributes for state management.
    """
    def wrapper(*args, **kwargs):
        # Call the factory function to get the target function with some closed-over state variables.
        fn = factory_fn(*args, **kwargs)
        
        # If the returned function is a functools.partial, unwrap it.
        if isinstance(fn, partial):
            actual = fn.func  # underlying function
            closure_vars = actual.__code__.co_freevars
            cells = actual.__closure__
            if not closure_vars or not cells:
                raise ValueError("Returned function has no closure variables")
            var_cell_map = dict(zip(closure_vars, cells))
            
            def set_state(**kwargs):
                """
                Update state variables in the function's closure.
                """
                for k, v in kwargs.items():
                    if k in var_cell_map:
                        var_cell_map[k].cell_contents = v

            @contextmanager
            def state(**kwargs):
                """
                A context manager to temporarily update state variables.
                """
                original = {k: var_cell_map[k].cell_contents for k in kwargs if k in var_cell_map}
                try:
                    set_state(**kwargs)
                    yield
                finally:
                    set_state(**original)
            
            def wrapped(*a, **kw):
                return fn(*a, **kw)
            
            # Attach state management functions to the wrapped callable.
            wrapped.set_state = set_state
            wrapped.state = state
            wrapped.get_state = lambda: {k: var_cell_map[k].cell_contents for k in closure_vars}
            return wrapped

        # Normal case: fn is a regular function.
        closure_vars = fn.__code__.co_freevars
        cells = fn.__closure__
        if not closure_vars or not cells:
            raise ValueError("Returned function has no closure variables")
        var_cell_map = dict(zip(closure_vars, cells))

        def set_state(**kwargs):
            """
            Update state variables in the function's closure.
            """
            for k, v in kwargs.items():
                if k in var_cell_map:
                    var_cell_map[k].cell_contents = v

        @contextmanager
        def state(**kwargs):
            """
            A context manager to temporarily update state variables.
            """
            original = {k: var_cell_map[k].cell_contents for k in kwargs if k in var_cell_map}
            try:
                set_state(**kwargs)
                yield
            finally:
                set_state(**original)

        # Attach the state management functions to the function as attributes.
        fn.set_state = set_state
        fn.state = state
        fn.get_state = lambda: {k: var_cell_map[k].cell_contents for k in closure_vars}

        return fn

    return wrapper


class StateContext:
    """
    A context manager to manage temporary states for multiple stateful functions.
    
    It accepts one or more pairs of (function, state_dict), where each function is expected
    to have been decorated with stateful_function (or provide a similar state context manager).
    When entering the context, the state of each function is temporarily updated based
    on the provided state_dict. Upon exiting, the original states are restored.
    
    Attributes:
        func_state_pairs (tuple): A tuple of (function, state_dict) pairs.
        _stack (ExitStack): A stack to manage multiple context managers for state restoration.
    
    Example:
        with StateContext((fn1, {'a': 1}), (fn2, {'b': 2})):
            # Within this block, fn1 and fn2 have their states updated.
            ...
        # Upon leaving the block, original states are automatically restored.
    """
    def __init__(self, *func_state_pairs):
        self.func_state_pairs = func_state_pairs
        self._stack = ExitStack()

    def __enter__(self):
        for fn, state_dict in self.func_state_pairs:
            try:
                self._stack.enter_context(fn.state(**state_dict))
            except AttributeError:
                pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stack.close()

