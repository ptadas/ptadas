# import pickle
#
#
# class Foo:
#     ac = {"a": 1, "b": 2}
#
#     def __init__(self):
#         self.ai = {"a": 1, "b": 2}
#
#
# first = Foo()
# pickled = pickle.dumps(first)
# print("fisrt dict", first.__dict__)
# print("pickled", pickled)
# second = pickle.loads(pickled)
#
# assert id(first) != id(second)
# assert id(first.ac) == id(second.ac)
# assert id(first.ai) != id(second.ai)


###############################################################################
# Asume this is a new module
import pickle


class Foo:
    pass


pickled = (
    b"\x80\x04\x950\x00\x00\x00\x00\x00\x00\x00\x8c\x08"
    b"__main__\x94\x8c\x03Foo\x94\x93\x94)\x81\x94}\x94\x8c"
    b"\x02ai\x94}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02usb."
)
first = pickle.loads(pickled)
# AttributeError: Can't get attribute 'Foo'
print("first.__dict__", first.__dict__)
