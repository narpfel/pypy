from rpython.rtyper.lltypesystem import lltype, rffi

CONSTANTS = [
    ('NULL', lambda space: None),
    ('None', lambda space: space.w_None),
    ('False', lambda space: space.w_False),
    ('True', lambda space: space.w_True),
    ('ValueError', lambda space: space.w_ValueError),
    ('TypeError', lambda space: space.w_TypeError),
    ('BaseObjectType', lambda space: space.w_object),
    ('TypeType', lambda space: space.w_type),
    ('LongType', lambda space: space.w_int),
    ('UnicodeType', lambda space: space.w_unicode),
    ('TupleType', lambda space: space.w_tuple),
    ('ListType', lambda space: space.w_list),
    ]


class HandleManager:

    def __init__(self, space):
        self.handles_w = [build_value(space) for name, build_value in CONSTANTS]
        self.release_callbacks = [None] * len(self.handles_w)
        self.free_list = []

    def new(self, w_object):
        if len(self.free_list) == 0:
            index = len(self.handles_w)
            self.handles_w.append(w_object)
            self.release_callbacks.append(None)
        else:
            index = self.free_list.pop()
            self.handles_w[index] = w_object
            # releasers[index] is already set to None by close()
        return index

    def close(self, index):
        assert index > 0
        if self.release_callbacks[index] is not None:
            w_obj = self.deref(index)
            for f in self.release_callbacks[index]:
                f.release(index, w_obj)
            self.release_callbacks[index] = None
        self.handles_w[index] = None
        self.free_list.append(index)

    def deref(self, index):
        assert index > 0
        return self.handles_w[index]

    def consume(self, index):
        """
        Like close, but also return the w_object which was pointed by the handled
        """
        assert index > 0
        w_object = self.handles_w[index]
        self.close(index)
        return w_object

    def dup(self, index):
        w_object = self.handles_w[index]
        return self.new(w_object)

    def attach_release_callback(self, index, cb):
        if self.release_callbacks[index] is None:
            self.release_callbacks[index] = [cb]
        else:
            self.release_callbacks[index].append(cb)


class HandleReleaseCallback(object):

    def release(self, h, w_obj):
        raise NotImplementedError


class FreeNonMovingBuffer(HandleReleaseCallback):
    """
    Callback to call rffi.free_nonmovingbuffer_ll
    """

    def __init__(self, llbuf, llstring, flag):
        self.llbuf = llbuf
        self.llstring = llstring
        self.flag = flag

    def release(self, h, w_obj):
        rffi.free_nonmovingbuffer_ll(self.llbuf, self.llstring, self.flag)



# =========================
# high level user interface
# =========================

def new(space, w_object):
    mgr = space.fromcache(HandleManager)
    return mgr.new(w_object)

def close(space, index):
    mgr = space.fromcache(HandleManager)
    mgr.close(index)

def deref(space, index):
    mgr = space.fromcache(HandleManager)
    return mgr.deref(index)

def consume(space, index):
    mgr = space.fromcache(HandleManager)
    return mgr.consume(index)

def dup(space, index):
    mgr = space.fromcache(HandleManager)
    return mgr.dup(index)

def attach_release_callback(space, index, cb):
    mgr = space.fromcache(HandleManager)
    return mgr.attach_release_callback(index, cb)

class using(object):
    """
    context-manager to new/close a handle
    """

    def __init__(self, space, w_object):
        self.space = space
        self.w_object = w_object
        self.h = -1

    def __enter__(self):
        self.h = new(self.space, self.w_object)
        return self.h

    def __exit__(self, etype, evalue, tb):
        close(self.space, self.h)
