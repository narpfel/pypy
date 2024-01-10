import os

from pypy.interpreter.gateway import interp2app
from pypy.interpreter.error import OperationError
from pypy.interpreter.baseobjspace import SpaceCache


class FrozenCache(SpaceCache):
    def __init__(self, space):
        mod = space.getbuiltinmodule('_frozen_importlib')
        self.w_frozen_import = mod.get('__import__')
        assert self.w_frozen_import is not None


class State:
    def __init__(self, space):
        self.cumulative_import_time = 0
        self.import_level = 0


def import_with_frames_removed(space, __args__):
    """__import__(name, globals=None, locals=None, fromlist=(), level=0) -> module
    
    Import a module. Because this function is meant for use by the Python
    interpreter and not for general use, it is better to use
    importlib.import_module() to programmatically import a module.
    
    The globals argument is only used to determine the context;
    they are not modified.  The locals argument is unused.  The fromlist
    should be a list of names to emulate ``from name import ...'', or an
    empty list to emulate ``import name''.
    When importing a module from a package, note that __import__('A.B', ...)
    returns package A when fromlist is empty, but its submodule B when
    fromlist is not empty.  The level argument is used to determine whether to
    perform absolute or relative imports: 0 is absolute, while a positive number
    is the number of parent directories to search relative to the current module."""
    from pypy.module.time.interp_time import perf_counter
    state = space.fromcache(State)
    stderr = 2

    old_cumulative_import_time = state.cumulative_import_time
    state.import_level += 1
    start = int(space.float_w(perf_counter(space)) * 1e6)
    state.cumulative_import_time = 0
    try:
        result = space.call_args(
            space.fromcache(FrozenCache).w_frozen_import, __args__)
    except OperationError as e:
        end = int(space.float_w(perf_counter(space)) * 1e6)
        import_time = end - start
        state.import_level -= 1
        state.cumulative_import_time = old_cumulative_import_time + import_time
        e.remove_traceback_module_frames(
              '<frozen importlib._bootstrap>',
              '<frozen importlib._bootstrap_external>',
              '<builtin>/frozen importlib._bootstrap_external')
        raise
    else:
        end = int(space.float_w(perf_counter(space)) * 1e6)
        import_time = end - start
        state.import_level -= 1
        format_string_args = [
            space.newint(import_time - state.cumulative_import_time),
            space.newint(import_time),
            space.newint(state.import_level * 2),
            space.newtext(""),
            __args__.firstarg(),
            space.newint(state.import_level),
        ]
        state.cumulative_import_time = old_cumulative_import_time + import_time
        format_string = space.newtext("import time: %9ld | %10ld | %*s%s %d\n")
        w_output = space.mod(format_string, space.newtuple(format_string_args))
        os.write(stderr, space.text_w(w_output))
        return result

import_with_frames_removed = interp2app(import_with_frames_removed,
                                        app_name='__import__')
