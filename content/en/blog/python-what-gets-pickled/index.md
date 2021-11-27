---
title: "Python what gets pickled"
description: "A quick dive into Pythons pickle protocol"
lead: "What does get pickled and what does not."
date: 2021-11-27T09:19:42+01:00
lastmod: 2021-11-27T09:19:42+01:00
draft: false
weight: 50
---


__TLDR__: For classes only the output of `<class instance>.__dict__` gets pickled. 

## Pickle

[Pickle](https://docs.python.org/3/library/pickle.html) module in Python implements a binary protocol to serialize and de-serialize a Python object. It is Python specific and as such only works in Python, but has the advantage of no dependencies on external standards such as JSON or XDR.

## Pickle example

```Python
import pickle


class Foo:
    ac = {"a": 1, "b": 2}

    def __init__(self):
        self.ai = {"a": 1, "b": 2}


first = Foo()
pickled = pickle.dumps(first)
second = pickle.loads(pickled)

assert id(first) != id(second)
assert id(first.ac) == id(second.ac)
assert id(first.ai) != id(second.ai)
```

First misconception I had, was that by pickling and unpickling a class I would create a new copy of the object and its attributes. Which is true as seen from `assert id(first) != id(second)`, however for some reason I also expected `assert id(first.ac) == id(second.ac)` to no be equal. I assumed that pickling would create a deepcopy of the object and when I unpickled it, all class objects even the class attribute will be unique. 

After a bit of contemplating this behavior makes sense, as that's what you would expect from a class attribute. This, however, made me wonder of what gets pickled. As stated in [docs](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled) `<...> classes whose __dict__ <...> is picklable <...>`. So how does it look in practice.

```python
print(first.__dict__)
>>> {'ai': {'a': 1, 'b': 2}}
``` 

Another example of what is being pickled can be seen running below code in a new module.

```python
import pickle
pickled = (
    b"\x80\x04\x950\x00\x00\x00\x00\x00\x00\x00\x8c\x08"
    b"__main__\x94\x8c\x03Foo\x94\x93\x94)\x81\x94}\x94\x8c"
    b"\x02ai\x94}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02usb."
)
first = pickle.loads(pickled)
```

Yet this would not work as `AttributeError: Can't get attribute 'Foo'` would get raised. If, however, we mock the class and try to unpickle all works as expected.

```python
import pickle


class Foo:
    pass


pickled = (
    b"\x80\x04\x950\x00\x00\x00\x00\x00\x00\x00\x8c\x08"
    b"__main__\x94\x8c\x03Foo\x94\x93\x94)\x81\x94}\x94\x8c"
    b"\x02ai\x94}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02usb."
)
first = pickle.loads(pickled)
print(first.__dict__)
>>> {'ai': {'a': 1, 'b': 2}}
```



