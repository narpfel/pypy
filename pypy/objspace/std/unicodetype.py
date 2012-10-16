from pypy.interpreter.error import OperationError, operationerrfmt
from pypy.interpreter.gateway import interp2app, unwrap_spec, WrappedDefault
from pypy.interpreter import unicodehelper
from pypy.objspace.std.stdtypedef import StdTypeDef, SMM
from pypy.objspace.std.register_all import register_all
from pypy.rlib.runicode import str_decode_utf_8, str_decode_ascii,\
     unicode_encode_utf_8, unicode_encode_ascii

from sys import maxint

def wrapunicode(space, uni):
    from pypy.objspace.std.unicodeobject import W_UnicodeObject
    from pypy.objspace.std.ropeunicodeobject import wrapunicode
    if space.config.objspace.std.withropeunicode:
        return wrapunicode(space, uni)
    return W_UnicodeObject(uni)

def plain_str2unicode(space, s):
    try:
        return unicode(s)
    except UnicodeDecodeError:
        for i in range(len(s)):
            if ord(s[i]) > 127:
                raise OperationError(
                    space.w_UnicodeDecodeError,
                    space.newtuple([
                    space.wrap('ascii'),
                    space.wrapbytes(s),
                    space.wrap(i),
                    space.wrap(i+1),
                    space.wrap("ordinal not in range(128)")]))
        assert False, "unreachable"


unicode_capitalize = SMM('capitalize', 1,
                         doc='S.capitalize() -> unicode\n\nReturn a'
                             ' capitalized version of S, i.e. make the first'
                             ' character\nhave upper case.')
unicode_center     = SMM('center', 3, defaults=(u' ',),
                         doc='S.center(width[, fillchar]) -> unicode\n\nReturn'
                             ' S centered in a Unicode string of length width.'
                             ' Padding is\ndone using the specified fill'
                             ' character (default is a space)')
unicode_count      = SMM('count', 4, defaults=(0, maxint),
                         doc='S.count(sub[, start[, end]]) -> int\n\nReturn'
                             ' the number of occurrences of substring sub in'
                             ' Unicode string\nS[start:end].  Optional'
                             ' arguments start and end are\ninterpreted as in'
                             ' slice notation.')
unicode_encode     = SMM('encode', 3, defaults=(None, None),
                         argnames=['encoding', 'errors'],
                         doc='S.encode([encoding[,errors]]) -> string or'
                             ' unicode\n\nEncodes S using the codec registered'
                             ' for encoding. encoding defaults\nto the default'
                             ' encoding. errors may be given to set a'
                             ' different error\nhandling scheme. Default is'
                             " 'strict' meaning that encoding errors raise\na"
                             ' UnicodeEncodeError. Other possible values are'
                             " 'ignore', 'replace' and\n'xmlcharrefreplace' as"
                             ' well as any other name registered'
                             ' with\ncodecs.register_error that can handle'
                             ' UnicodeEncodeErrors.')
unicode_expandtabs = SMM('expandtabs', 2, defaults=(8,),
                         doc='S.expandtabs([tabsize]) -> unicode\n\nReturn a'
                             ' copy of S where all tab characters are expanded'
                             ' using spaces.\nIf tabsize is not given, a tab'
                             ' size of 8 characters is assumed.')
unicode_format     = SMM('format', 1, general__args__=True,
                         doc='S.format() -> new style formating')
unicode_isalnum    = SMM('isalnum', 1,
                         doc='S.isalnum() -> bool\n\nReturn True if all'
                             ' characters in S are alphanumeric\nand there is'
                             ' at least one character in S, False otherwise.')
unicode_isalpha    = SMM('isalpha', 1,
                         doc='S.isalpha() -> bool\n\nReturn True if all'
                             ' characters in S are alphabetic\nand there is at'
                             ' least one character in S, False otherwise.')
unicode_isdecimal  = SMM('isdecimal', 1,
                         doc='S.isdecimal() -> bool\n\nReturn True if there'
                             ' are only decimal characters in S,\nFalse'
                             ' otherwise.')
unicode_isdigit    = SMM('isdigit', 1,
                         doc='S.isdigit() -> bool\n\nReturn True if all'
                             ' characters in S are digits\nand there is at'
                             ' least one character in S, False otherwise.')
unicode_islower    = SMM('islower', 1,
                         doc='S.islower() -> bool\n\nReturn True if all cased'
                             ' characters in S are lowercase and there is\nat'
                             ' least one cased character in S, False'
                             ' otherwise.')
unicode_isnumeric  = SMM('isnumeric', 1,
                         doc='S.isnumeric() -> bool\n\nReturn True if there'
                             ' are only numeric characters in S,\nFalse'
                             ' otherwise.')
unicode_isspace    = SMM('isspace', 1,
                         doc='S.isspace() -> bool\n\nReturn True if all'
                             ' characters in S are whitespace\nand there is at'
                             ' least one character in S, False otherwise.')
unicode_istitle    = SMM('istitle', 1,
                         doc='S.istitle() -> bool\n\nReturn True if S is a'
                             ' titlecased string and there is at least'
                             ' one\ncharacter in S, i.e. upper- and titlecase'
                             ' characters may only\nfollow uncased characters'
                             ' and lowercase characters only cased'
                             ' ones.\nReturn False otherwise.')
unicode_isupper    = SMM('isupper', 1,
                         doc='S.isupper() -> bool\n\nReturn True if all cased'
                             ' characters in S are uppercase and there is\nat'
                             ' least one cased character in S, False'
                             ' otherwise.')
unicode_isidentifier = SMM('isidentifier', 1,
                         doc='S.isidentifier() -> bool\n\nReturn True if S is'
                             ' a valid identifier according\nto the language'
                             ' definition.')
unicode_isprintable  = SMM('isprintable', 1,
                           doc='S.isprintable() -> bool\n\nReturn True if all'
                               ' characters in S are considered printable in'
                               ' repr or S is empty, False otherwise')
unicode_join       = SMM('join', 2,
                         doc='S.join(sequence) -> unicode\n\nReturn a string'
                             ' which is the concatenation of the strings in'
                             ' the\nsequence.  The separator between elements'
                             ' is S.')
unicode_ljust      = SMM('ljust', 3, defaults=(u' ',),
                         doc='S.ljust(width[, fillchar]) -> int\n\nReturn S'
                             ' left justified in a Unicode string of length'
                             ' width. Padding is\ndone using the specified'
                             ' fill character (default is a space).')
unicode_lower      = SMM('lower', 1,
                         doc='S.lower() -> unicode\n\nReturn a copy of the'
                             ' string S converted to lowercase.')
unicode_rjust      = SMM('rjust', 3, defaults=(u' ',),
                         doc='S.rjust(width[, fillchar]) -> unicode\n\nReturn'
                             ' S right justified in a Unicode string of length'
                             ' width. Padding is\ndone using the specified'
                             ' fill character (default is a space).')
unicode_swapcase   = SMM('swapcase', 1,
                         doc='S.swapcase() -> unicode\n\nReturn a copy of S'
                             ' with uppercase characters converted to'
                             ' lowercase\nand vice versa.')
unicode_title      = SMM('title', 1,
                         doc='S.title() -> unicode\n\nReturn a titlecased'
                             ' version of S, i.e. words start with title'
                             ' case\ncharacters, all remaining cased'
                             ' characters have lower case.')
unicode_translate  = SMM('translate', 2,
                         doc='S.translate(table) -> unicode\n\nReturn a copy'
                             ' of the string S, where all characters have been'
                             ' mapped\nthrough the given translation table,'
                             ' which must be a mapping of\nUnicode ordinals to'
                             ' Unicode ordinals, Unicode strings or'
                             ' None.\nUnmapped characters are left untouched.'
                             ' Characters mapped to None\nare deleted.')
unicode_upper      = SMM('upper', 1,
                         doc='S.upper() -> unicode\n\nReturn a copy of S'
                             ' converted to uppercase.')
unicode_zfill      = SMM('zfill', 2,
                         doc='S.zfill(width) -> unicode\n\nPad a numeric'
                             ' string x with zeros on the left, to fill a'
                             ' field\nof the specified width. The string x is'
                             ' never truncated.')

# stuff imported from stringtype for interoperability

from pypy.objspace.std.stringtype import str_endswith as unicode_endswith
from pypy.objspace.std.stringtype import str_startswith as unicode_startswith
from pypy.objspace.std.stringtype import str_find as unicode_find
from pypy.objspace.std.stringtype import str_index as unicode_index
from pypy.objspace.std.stringtype import str_replace as unicode_replace
from pypy.objspace.std.stringtype import str_rfind as unicode_rfind
from pypy.objspace.std.stringtype import str_rindex as unicode_rindex
from pypy.objspace.std.stringtype import str_split as unicode_split
from pypy.objspace.std.stringtype import str_rsplit as unicode_rsplit
from pypy.objspace.std.stringtype import str_partition as unicode_partition
from pypy.objspace.std.stringtype import str_rpartition as unicode_rpartition
from pypy.objspace.std.stringtype import str_splitlines as unicode_splitlines
from pypy.objspace.std.stringtype import str_strip as unicode_strip
from pypy.objspace.std.stringtype import str_rstrip as unicode_rstrip
from pypy.objspace.std.stringtype import str_lstrip as unicode_lstrip

# ____________________________________________________________

def getdefaultencoding(space):
    return space.sys.defaultencoding

def _get_encoding_and_errors(space, w_encoding, w_errors):
    if space.is_none(w_encoding):
        encoding = None
    else:
        encoding = space.str_w(w_encoding)
    if space.is_none(w_errors):
        errors = None
    else:
        errors = space.str_w(w_errors)
    return encoding, errors

def encode_object(space, w_object, encoding, errors):
    if encoding is None:
        # Get the encoder functions as a wrapped object.
        # This lookup is cached.
        w_encoder = space.sys.get_w_default_encoder()
    else:
        if errors is None or errors == 'strict':
            if encoding == 'ascii':
                u = space.unicode_w(w_object)
                eh = unicodehelper.encode_error_handler(space)
                return space.wrapbytes(unicode_encode_ascii(
                        u, len(u), None, errorhandler=eh))
            if encoding == 'utf-8':
                u = space.unicode_w(w_object)
                eh = unicodehelper.encode_error_handler(space)
                return space.wrapbytes(unicode_encode_utf_8(
                        u, len(u), None, errorhandler=eh,
                        allow_surrogates=True))
        from pypy.module._codecs.interp_codecs import lookup_codec
        w_encoder = space.getitem(lookup_codec(space, encoding), space.wrap(0))
    if errors is None:
        w_errors = space.wrap('strict')
    else:
        w_errors = space.wrap(errors)
    w_restuple = space.call_function(w_encoder, w_object, w_errors)
    w_retval = space.getitem(w_restuple, space.wrap(0))
    if not space.isinstance_w(w_retval, space.w_bytes):
        raise operationerrfmt(space.w_TypeError,
            "encoder did not return a bytes string (type '%s')",
            space.type(w_retval).getname(space))
    return w_retval

def decode_object(space, w_obj, encoding, errors):
    if encoding is None:
        encoding = getdefaultencoding(space)
    if errors is None or errors == 'strict':
        if encoding == 'ascii':
            # XXX error handling
            s = space.bufferstr_w(w_obj)
            eh = unicodehelper.decode_error_handler(space)
            return space.wrap(str_decode_ascii(
                    s, len(s), None, final=True, errorhandler=eh)[0])
        if encoding == 'utf-8':
            s = space.bufferstr_w(w_obj)
            eh = unicodehelper.decode_error_handler(space)
            return space.wrap(str_decode_utf_8(
                    s, len(s), None, final=True, errorhandler=eh)[0])
    w_codecs = space.getbuiltinmodule("_codecs")
    w_decode = space.getattr(w_codecs, space.wrap("decode"))
    if errors is None:
        w_retval = space.call_function(w_decode, w_obj, space.wrap(encoding))
    else:
        w_retval = space.call_function(w_decode, w_obj, space.wrap(encoding),
                                       space.wrap(errors))
    return w_retval


def unicode_from_encoded_object(space, w_obj, encoding, errors):
    w_retval = decode_object(space, w_obj, encoding, errors)
    if not space.isinstance_w(w_retval, space.w_unicode):
        raise operationerrfmt(space.w_TypeError,
            "decoder did not return an unicode object (type '%s')",
            space.type(w_retval).getname(space))
    return w_retval

def unicode_from_object(space, w_obj):
    if space.is_w(space.type(w_obj), space.w_unicode):
        return w_obj

    w_unicode_method = space.lookup(w_obj, "__str__")
    return space.repr(w_obj) if w_unicode_method is None else space.str(w_obj)

@unwrap_spec(w_object = WrappedDefault(u''))
def descr_new_(space, w_unicodetype, w_object=None, w_encoding=None,
               w_errors=None):
    # NB. the default value of w_obj is really a *wrapped* empty string:
    #     there is gateway magic at work
    from pypy.objspace.std.unicodeobject import W_UnicodeObject
    from pypy.objspace.std.ropeunicodeobject import W_RopeUnicodeObject
    w_obj = w_object

    encoding, errors = _get_encoding_and_errors(space, w_encoding, w_errors)
    if encoding is None and errors is None:
        w_value = unicode_from_object(space, w_obj)
    else:
        w_value = unicode_from_encoded_object(space, w_obj,
                                              encoding, errors)
    if space.is_w(w_unicodetype, space.w_unicode):
        return w_value

    if space.config.objspace.std.withropeunicode:
        assert isinstance(w_value, W_RopeUnicodeObject)
        w_newobj = space.allocate_instance(W_RopeUnicodeObject, w_unicodetype)
        W_RopeUnicodeObject.__init__(w_newobj, w_value._node)
        return w_newobj

    assert isinstance(w_value, W_UnicodeObject)
    w_newobj = space.allocate_instance(W_UnicodeObject, w_unicodetype)
    W_UnicodeObject.__init__(w_newobj, w_value._value)
    return w_newobj

def descr_maketrans(space, w_type, w_x, w_y=None, w_z=None):
    """str.maketrans(x[, y[, z]]) -> dict (static method)

    Return a translation table usable for str.translate().
    If there is only one argument, it must be a dictionary mapping Unicode
    ordinals (integers) or characters to Unicode ordinals, strings or None.
    Character keys will be then converted to ordinals.
    If there are two arguments, they must be strings of equal length, and
    in the resulting dictionary, each character in x will be mapped to the
    character at the same position in y. If there is a third argument, it
    must be a string, whose characters will be mapped to None in the result."""

    if space.is_none(w_y):
        y = None
    else:
        y = space.unicode_w(w_y)
    if space.is_none(w_z):
        z = None
    else:
        z = space.unicode_w(w_z)

    w_new = space.newdict()
    if y is not None:
        # x must be a string too, of equal length
        ylen = len(y)
        try:
            x = space.unicode_w(w_x)
        except OperationError, e:
            if not e.match(space, space.w_TypeError):
                raise
            raise OperationError(space.w_TypeError, space.wrap(
                    "first maketrans argument must "
                    "be a string if there is a second argument"))
        if len(x) != ylen:
            raise OperationError(space.w_ValueError, space.wrap(
                    "the first two maketrans "
                    "arguments must have equal length"))
        # create entries for translating chars in x to those in y
        for i in range(len(x)):
            w_key = space.newint(ord(x[i]))
            w_value = space.newint(ord(y[i]))
            space.setitem(w_new, w_key, w_value)
        # create entries for deleting chars in z
        if z is not None:
            for i in range(len(z)):
                w_key = space.newint(ord(z[i]))
                space.setitem(w_new, w_key, space.w_None)
    else:
        # x must be a dict
        if not space.is_w(space.type(w_x), space.w_dict):
            raise OperationError(space.w_TypeError, space.wrap(
                    "if you give only one argument "
                    "to maketrans it must be a dict"))
        # copy entries into the new dict, converting string keys to int keys
        w_iter = space.call_method(w_x, "iteritems")
        while True:
            try:
                w_item = space.next(w_iter)
            except OperationError, e:
                if not e.match(space, space.w_StopIteration):
                    raise
                break
            w_key, w_value = space.unpackiterable(w_item, 2)
            if space.isinstance_w(w_key, space.w_unicode):
                # convert string keys to integer keys
                key = space.unicode_w(w_key)
                if len(key) != 1:
                    raise OperationError(space.w_ValueError, space.wrap(
                            "string keys in translate "
                            "table must be of length 1"))
                w_key = space.newint(ord(key[0]))
            else:
                # just keep integer keys
                try:
                    space.int_w(w_key)
                except OperationError, e:
                    if not e.match(space, space.w_TypeError):
                        raise
                    raise OperationError(space.w_TypeError, space.wrap(
                            "keys in translate table must "
                            "be strings or integers"))
            space.setitem(w_new, w_key, w_value)
    return w_new

# ____________________________________________________________

unicode_typedef = StdTypeDef("str",
    __new__ = interp2app(descr_new_),
    __doc__ = '''str(string [, encoding[, errors]]) -> object

Create a new string object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.''',
    maketrans = interp2app(descr_maketrans, as_classmethod=True),
    )

unicode_typedef.registermethods(globals())

unitypedef = unicode_typedef
register_all(vars(), globals())
