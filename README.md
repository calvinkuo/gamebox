# gamebox
 Rewrite of the gamebox library used at UVA

The goal of this project is to modernize gamebox using [type annotations](https://docs.python.org/3/library/typing.html)
and [managed attributes](https://docs.python.org/3/howto/descriptor.html#managed-attributes) to create a more idiomatic
and maintainable library that takes advantage of modern Python syntax.


## Why make these changes?
PyCharm, the IDE used in CS 111x, can provide warnings when functions are called with parameters of the wrong type.
Additionally, it can autocomplete the names of class/instance methods and properties, as well as infer their types.

As Python is a dynamic language, to take full advantage of these features, libraries must provide that information
in the correct format. Python 3.5 introduced type hints, which allow variable types, argument types, and return types 
to be specified explicitly.

By adding full type hints to the library, student code will display warnings within the IDE if functions are called with
incorrect parameters, even when the students do not use type annotations in their own code. Similarly, when attributes
are defined using the managed attribute syntax, the IDE will also be able to determine the types of them, and warn if
they are used incorrectly. This matches the behavior that students would expect from the standard library methods that
they are familiar with.


## Contents
This repository contains drop-in replacements for previous versions of the library:
* [gamebox_compat_ge.py](gamebox_compat_ge.py) is a drop-in replacement for the UVA Game Engine, which was used in the
  Fall 2022 semester (compatible with Python 3.7+)
* Drop-in replacements for the version of gamebox.py used from Spring 2018 through Summer 2022:
  * [gamebox_compat.py](gamebox_compat.py) (compatible with Python 3.9+)
  * [gamebox_compat_37.py](gamebox_compat_37.py) (compatible with Python 3.7+)
* [gamebox_compat_uni.py](gamebox_compat_uni.py) is a universal drop-in replacement for both the UVA Game Engine and
  gamebox.py (compatible with Python 3.7+)
* [gamebox_legacy.py](gamebox_legacy.py) is the legacy version of gamebox used from Spring 2018 through Summer 2022
  (compatible with both Python 2 and Python 3)

### Sample projects
* [sample.py](sample.py), an example project using gamebox
* [sample_ge.py](sample_ge.py), an example project using the UVA Game Engine


## History
gamebox was originally written by Luther Tychonievich for the CS 111x course during the Fall 2015 semester,
when the course switched from using Java to Python. At the time, the latest version of Python was 3.4.3.
In Spring 2018, sound and font support were removed from the library, and it remained unchanged until Fall 2022,
when several changes were made by Adam Dirting, and it was renamed the UVA Game Engine.


## Changelog
### Changes between gamebox and UVA Game Engine
* Drops support for Python 2
* Wraps exception returned when a filepath/URL for an image is incorrect instead of always raising a `urllib` error
* Adds `keys` and `key_constants` as public global variables
* Adds a new method `is_pressing(key)`
* Changes the expected signature of the `callback` parameter in `timer_loop(fps, callback, limit=None)`
  from `callback(keys)` to `callback()`

This last change is a breaking change that affects games and examples made with earlier versions of gamebox.
[gamebox_compat_uni.py](gamebox_compat_uni.py) inspects the function signature of `callback` and provides the `keys`
parameter only if needed, so it is backwards-compatible with both versions.
